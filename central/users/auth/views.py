import jwt
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponsePermanentRedirect
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response
from .serializers import (
    GoogleAuthSerializer,
    AppleAuthSerializer,
    PhoneVerifySerializer,
    RegisterSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    LogoutSerializer,
    PhoneAuthSerializer,
    ResendOTPSerializer,
)
from django.utils.translation import gettext_lazy as _
from users.models import User
from users.utils import verify_token, check_username, send_otp
from .services import ClanAuthService


class Register(generics.GenericAPIView):
    """
    View for registering staff or clan members
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            renderer_context = {"message": response.get("message")}
            return Response(response.data, status=status.HTTP_201_CREATED)

        return Response(
            {"message": _("Invalid data"), "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CardID(generics.GenericAPIView):
    pass


class PhoneAuth(generics.GenericAPIView):
    serializer_class = PhoneAuthSerializer
    permission_classes = [permissions.AllowAny]

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
    serializer_class = PhoneVerifySerializer

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
        if stored_otp == otp:
            user, created = User.objects.get_or_create(
                phone_number=serializer.validated_data["phone_number"]
            )
            if created:
                if not user.password:
                    user.set_unusable_password()
                if not user.email:
                    user.email = phone_number + "@clan.sa"
                if not user.username:
                    user.username = phone_number
                user.phone_number_authentication = True
                user.is_phone_number_verified = True
                user.save()

            return Response(
                {"message": _("Successfully verified")}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": _("this otp code is incorrect")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailVerify(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": _("Successfully verified")}, status=status.HTTP_200_OK
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


class Login(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        response_data = user.tokens()
        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetRequest(generics.GenericAPIView):
    """
    View to handle password reset OTP request
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "OTP has been sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    """
    View to handle password reset confirmation using OTP
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )


class Logout(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GoogleAuth(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.user
        if serializer.is_valid():
            id_token = serializer.validated_data["id_token"]

            try:
                user = ClanAuthService.link_google_account(user, id_token)
                tokens = user.tokens()

                return Response(
                    {
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
    permission_classes = [permissions.AllowAny]
    serializer_class = AppleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_token = serializer.validated_data["id_token"]

            try:
                apple_data = jwt.decode(id_token, options={"verify_signature": False})

                email = apple_data.get("email")
                first_name = apple_data.get("given_name")
                last_name = apple_data.get("family_name")
                apple_id = apple_data.get("sub")

                user, created = User.objects.get_or_create(
                    apple_id=apple_id,
                    defaults={
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "apple_authentication": True,
                        "is_active": True,
                    },
                )

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


class ClanUserStatus(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        actions = []
        user = request.user
        if not user.is_email_verified:
            actions.append({"email_verify": ""})
