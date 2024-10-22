from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from google.auth.exceptions import GoogleAuthError


class GoogleService:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, Request())

            if id_info.get('iss') != 'accounts.google.com':
                raise AuthenticationFailed(_('Invalid token issuer.'))

            if not id_info.get('sub') or id_info.get('aud') != settings.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed(_('Could not verify user.'))

            return id_info

        except GoogleAuthError as e:
            raise ValidationError(_("Google token verification failed: {0}".format(str(e))))

        except Exception as e:
            raise Exception(_('An error occurred during token validation: {0}'.format(str(e))))


class AppleService:
    @staticmethod
    def validate(access_token):
        pass
