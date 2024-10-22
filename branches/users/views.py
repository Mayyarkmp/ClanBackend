from django.db import IntegrityError

from branches.users.models.branch_user import Status
from .models import BranchUser, Manager, Delivery, Preparer, Staff, WorkPeriod, Zone
from rest_framework.response import Response
from customers.auth.views import PhoneVerify
from rest_framework import status
from .serializers import (
    BranchUserSerializer,
    ManagerBranchMergingSerializer,
    ManagerSerializer,
    DeliverySerializer,
    PreparerSerializer,
    StaffSerializer,
    WorkPeriodSerializer,
    ZoneSerializer,
)
from users.auth.serializers import GoogleAuthSerializer, AppleAuthSerializer
from core.base.viewsets import SuperModelViewSet
from customers.auth.serializers import (
    PhoneAuthenticationSerializer,
    PhoneNumberVerificationSerializer,
)
from users.utils import send_otp, verify_token
from django.core.cache import cache
from users.auth.services import GoogleService


class BranchUserViewSet(SuperModelViewSet):
    queryset = BranchUser.objects.all()
    serializer_class = BranchUserSerializer


class ManagerViewSet(SuperModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerBranchMergingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            branch = serializer.validated_data["branchSerializer"]
            if branch is not None:
                manager = serializer.validated_data["managerSerializer"]
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"message": "manager needs to rigester branch"},
                status=status.HTTP_400_BAD_REQUEST,
            )  # here we need to check the status code that we want to return

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def SendOtpToPhoneNumber(self, request, *args, **kwargs):
        data = request.data
        serializer = PhoneAuthenticationSerializer.get_serializer(data=data)
        if serializer.is_valid():
            phoneNumber = serializer.validated_data.get("phoneNumber")
            token, otp = send_otp(phoneNumber, is_email=False)
            cache.set(f"otp_{phoneNumber}", otp, timeout=120)
            return Response({"token": token, "timeout": 120}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verfiyPhoneNumber(self, request, *args, **kwargs):
        data = request.data
        serializer = PhoneNumberVerificationSerializer.get_serializer(data=data)
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
                manager, created = Manager.objects.get_or_create(
                    phone_number=serializer.validated_data["phone_number"],
                    username=phone_number,
                    email=f"{phone_number}@clan.sa",
                )
                if created:
                    manager.set_unusable_password()
                    manager.phone_number_authentication = True
                    manager.is_phone_number_verified = True
                    manager.is_active = True
                    manager.save()
            except IntegrityError as e:
                print(e)
                manager = Manager.objects.get(
                    phone_number=serializer.validated_data["phone_number"]
                )
                # TODO: we reviewed with this

                # manager.is_phone_number_verified = True
                # manager.is_active = True
                # manager.save()

            return Response(
                {"message": ("Successfully verified"), "tokens": manager.tokens()},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": ("this otp code is incorrect")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def verfiyEmail(self, request, *args, **kwargs):
        serializer_class = GoogleAuthSerializer
        serializer = serializer_class(data=request.data)
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
                user, created = Manager.objects.get_or_create(
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

    def login(self, request):
        serializer_class = ManagerSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Authenticate the manager (you might want to use a custom authentication logic here)
            try:
                manager = Manager.objects.get(email=email)

                if not manager.check_password(password):
                    return Response(
                        {"error": "Invalid credentials"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if manager.status == Status.ACTIVE:
                    return Response(
                        {"tokens": manager.tokens()}, status=status.HTTP_200_OK
                    )
                elif manager.status == Status.REVIEWING:
                    return Response(
                        {"message": "Your account is under review."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                else:
                    return Response(
                        {
                            "message": "Your account has another problem, blocked, inactive or stopped."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            except Manager.DoesNotExist:
                return Response(
                    {"error": "Manager does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryViewSet(SuperModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class PreparerViewSet(SuperModelViewSet):
    queryset = Preparer.objects.all()
    serializer_class = PreparerSerializer


class StaffViewSet(SuperModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class WorkPeriodViewSet(SuperModelViewSet):
    queryset = WorkPeriod.objects.all()
    serializer_class = WorkPeriodSerializer


class ZoneViewSet(SuperModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
