from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from customers.models import Customer
from users.utils import send_otp


class PhoneAuthenticationSerializer(serializers.Serializer):
    """
        Serializer of Register or Login Customer use phone number
    """
    phone_number = PhoneNumberField()


class PhoneNumberVerificationSerializer(serializers.Serializer):
    """
    Serializer for phone number verification
    """
    phone_number = PhoneNumberField()
    otp = serializers.CharField(max_length=6)
    token = serializers.CharField()


class ResendOTPSerializer(serializers.Serializer):
    """
    Serializer for resending OTP to phone number.
    """

    phone_number = PhoneNumberField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        try:
            customer, created = Customer.objects.get_or_create(phone_number=phone_number)
            phone_number = phone_number.as_international.replace(" ", "")
            token_phone, otp_phone = send_otp(phone_number, is_email=False)
            attrs['token'] = token_phone if token_phone else None
            attrs["message"] = _("OTP sent to phone number successfully.")
            return attrs
        except Exception as e:
            raise ValueError(_('Error sending OTP to phone number'))


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

