import random

import jwt
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .serializers import (
    PhoneAuthenticationSerializer,
    PhoneNumberVerificationSerializer,
    ResendOTPSerializer,
)
from users.auth.serializers import GoogleAuthSerializer, AppleAuthSerializer
from users.auth.services import GoogleService
from ..models import Customer
from users.utils import send_otp, verify_token


class PhoneAuth(generics.GenericAPIView):
    serializer_class = PhoneAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data[
            "phone_number"
        ].as_international.replace(" ", "")
        token, otp = send_otp(phone_number, is_email=False)
        cache.set(f"otp_{phone_number}", otp, timeout=120)
        return Response({"token": token, "timeout": 120}, status=status.HTTP_200_OK)


class PhoneVerify(generics.GenericAPIView):
    serializer_class = PhoneNumberVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data[
            "phone_number"
        ].as_international.replace(" ", "")
        otp = serializer.validated_data["otp"]
        token = serializer.validated_data["token"]

        verified_phone = verify_token(token)
        if verified_phone != phone_number:
            return Response(
                {"error": "this key is incorrect"}, status=status.HTTP_400_BAD_REQUEST
            )

        stored_otp = cache.get(f"otp_{phone_number}")
        print(phone_number)
        if stored_otp == otp:
            cache.delete(f"otp_{phone_number}")
            try:
                customer, created = Customer.objects.get_or_create(
                    phone_number=serializer.validated_data["phone_number"],
                    username=phone_number,
                    email=f"{phone_number}@clan.sa",
                )
                if created:
                    customer.set_unusable_password()
                    customer.phone_number_authentication = True
                    customer.is_phone_number_verified = True
                    customer.is_active = True
                    customer.save()
            except IntegrityError as e:
                print(e)
                customer = Customer.objects.get(
                    phone_number=serializer.validated_data["phone_number"]
                )
            return Response(
                {"message": _("Successfully verified"), "tokens": customer.tokens()},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": _("this otp code is incorrect")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendOTP(generics.GenericAPIView):
    """
    View for resending OTP to email or phone number.
    """

    serializer_class = ResendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get("message")
        token = serializer.validated_data.get("token")
        if token:
            return Response(
                {
                    "message": message,
                    "data": {
                        "token": token,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": _("Error sending OTP")}, status=status.HTTP_400_BAD_REQUEST
        )


class GoogleAuth(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data["access_token"]

            try:
                user_data = GoogleService.validate(access_token)

                # Extract user info
                google_id = user_data.get("sub")
                email = user_data.get("email")
                first_name = user_data.get("given_name", "")
                last_name = user_data.get("family_name", "")

                # Create or get the user
                user, created = Customer.objects.get_or_create(
                    email=email,
                    defaults={
                        "google_id": google_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "google_authentication": True,
                    },
                )
                user.is_email_verified = True

                # Generate tokens (Assuming user has a method to generate tokens)
                tokens = user.tokens()

                return Response(
                    {
                        "message": "Authentication successful",
                        "tokens": tokens,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            except ValueError as e:
                # Invalid token
                return Response(
                    {"error": "Invalid Google token", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppleAuth(generics.GenericAPIView):
    serializer_class = AppleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data["access_token"]

            try:
                apple_data = jwt.decode(
                    access_token, options={"verify_signature": False}
                )

                email = apple_data.get("email")
                first_name = apple_data.get("given_name")
                last_name = apple_data.get("family_name")
                apple_id = apple_data.get("sub")
                user, created = Customer.objects.get_or_create(
                    apple_id=apple_id,
                    defaults={
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "apple_authentication": True,
                        "is_active": True,
                    },
                )

                user.is_email_verified = True
                if not created:
                    user.apple_authentication = True
                    user.save()

                tokens = user.tokens()

                return Response(
                    {"message": "Authentication successful", "tokens": tokens},
                    status=status.HTTP_200_OK,
                )
            except jwt.ExpiredSignatureError:
                return Response(
                    {"error": "Apple token has expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except jwt.DecodeError:
                return Response(
                    {"error": "Invalid Apple token"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
