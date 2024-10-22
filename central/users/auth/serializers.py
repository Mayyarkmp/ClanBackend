from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from users.utils import check_username, check_user_email, check_user_phone_number, send_otp, verify_token
from central.users.models import CentralUser
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    """
        Serializer for registering a ClanUser.
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)

    class Meta:
        model = CentralUser
        fields = ['email', "username", 'phone_number', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        username = attrs.get('username')

        # Validate email presence
        if not email:
            raise serializers.ValidationError({"email": _("Email is required")})

        # Validate phone number presence
        if not phone_number:
            raise serializers.ValidationError({"phone_number": _("Phone number is required.")})

        # Check for existing email
        if check_user_email(email):
            raise serializers.ValidationError({"email": _("Email already registered")})

        # Check for existing phone number
        if check_user_phone_number(phone_number):
            raise serializers.ValidationError({"phone_number": _("This phone number is already used in another account")})

        # Check for existing username
        if check_username(username):
            raise serializers.ValidationError({"username": _("Username is already taken")})

        return attrs

    def create(self, validated_data):
        try:
            # Create the user
            user = CentralUser.objects.create_user(**validated_data)
        except Exception as e:
            raise serializers.ValidationError({"detail": _("Error creating user: ") + str(e)})

        # Send OTP for email and phone number
        email_token, phone_token = None, None

        if user:
            # Send email OTP
            try:
                email_token, otp_email = send_otp(user.email, is_email=True)
            except Exception:
                raise serializers.ValidationError({"detail": _("Error creating email token")})

            # Send phone OTP
            try:
                phone_number = user.phone_number.as_international.replace(" ", "")
                phone_token, otp_phone = send_otp(phone_number, is_email=False)
            except Exception:
                raise serializers.ValidationError({"detail": _("Error creating phone token")})

        # Return the response data (this would usually be returned in the view)
        return {
            "message": _("User registered successfully. Please verify your account."),
            "data": {
                'email_token': email_token,
                'phone_token': phone_token,
                "timeout": 120
            }
        }


class PhoneAuthSerializer(serializers.Serializer):
    """
        Serializer of Register or Login Customer use phone number
    """
    phone_number = PhoneNumberField()


class PhoneVerifySerializer(serializers.Serializer):
    """
    Serializer for phone number verification
    """
    phone_number = PhoneNumberField()
    otp = serializers.CharField(max_length=6)
    token = serializers.CharField()


class EmailVerifySerializer(serializers.Serializer):
    """
        Serializer for email verification
    """
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    token = serializers.CharField(max_length=555)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        token = attrs.get('token')
        verified_email = verify_token(token, True)
        if verified_email != email:
            raise AuthenticationFailed('this key is incorrect')
        stored_otp = cache.get(f"otp_{email}")
        if stored_otp == otp:
            user = CentralUser.objects.get(email=email)

            if user:
                user.is_verified = True
                user.email_authentication = True
                user.is_email_verified = True
                user.save()
            attrs['user'] = user
            return attrs

        else:
            raise AuthenticationFailed(_('this otp code is incorrect'))


class ResendOTPSerializer(serializers.Serializer):
    """
    Serializer for resending OTP to email or phone number.
    """
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        if not email and not phone_number:
            raise serializers.ValidationError(_("Please provide either email or phone number."))

        if email and phone_number:
            raise serializers.ValidationError(_("Provide either email or phone number, not both."))

        if email and not check_user_email(email):
            raise serializers.ValidationError(_("Email not registered."))

        if phone_number and not check_user_phone_number(phone_number):
            raise serializers.ValidationError(_("Phone number not registered."))

        if email:
            try:
                user = CentralUser.objects.get(email=email)
                if user.is_email_verified:
                    raise ValueError(_("This Email is already verified"))
                token_email, otp_email = send_otp(email, is_email=True)
                attrs['token'] = token_email if token_email else None
                attrs["message"] = _("OTP sent to Email successfully.")
                return attrs
            except Exception as e:
                raise ValueError(_("Error sending OTP to email"))

        if phone_number:
            try:
                user = CentralUser.objects.get(phone_number=phone_number)
                if user.is_phone_number_verified:
                    raise ValueError(_("This Phone Number is already verified"))
                phone_number = phone_number.as_international.replace(" ", "")
                token_phone, otp_phone = send_otp(phone_number, is_email=False)
                attrs['token'] = token_phone if token_phone else None
                attrs["message"] = _("OTP sent to phone number successfully.")
                return attrs
            except Exception as e:
                raise ValueError(_('Error sending OTP to phone number'))


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = CentralUser
        fields = ['email', 'password', 'tokens', 'status']

    def get_tokens(self, obj):
        user = CentralUser.objects.get(email=obj['email'])
        return user.tokens()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(_('Invalid credentials, try again.'))
        # if user.polymorphic_ctype.model != "centraluser":
        #     raise AuthenticationFailed(_('User does not have the required permissions.'))

        # if user.status != "ACTIVE":
        #     raise AuthenticationFailed(_('Account disabled, contact admin.'))
        # if not user.is_email_verified and not user.is_phone_number_verified:
        #     raise AuthenticationFailed(_('Email or phone number is not verified.'))


        attrs['user'] = user
        return attrs


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)


class AppleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = CentralUser.objects.get(email=email)
        except CentralUser.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address.")
        return email

    def save(self):
        email = self.validated_data['email']
        user = CentralUser.objects.get(email=email)

        token, otp = send_otp(email, is_email=True)

        cache.set(f"otp_{email}", otp, timeout=300)
        return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        cached_otp = cache.get(f"otp_{email}")
        if cached_otp is None or cached_otp != otp:
            raise serializers.ValidationError("Invalid or expired OTP.")

        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        try:
            user = CentralUser.objects.get(email=email)
        except CentralUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        user.set_password(new_password)
        user.save()

        cache.delete(f"otp_{email}")

        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
