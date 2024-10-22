import jwt
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponsePermanentRedirect
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response

from django.utils.translation import gettext_lazy as _
from users.models import User
from users.utils import verify_token, check_username, send_otp



class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [settings.APP_SCHEME, 'http', 'https']


class CheckUserNameView(views.APIView):

    def get(self, request):
        username = request.query_params.get('username', None)
        if username is None:
            return Response({'error': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)

        username_already_use = check_username(username)
        if username_already_use:
            return Response({'error': 'username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'username': username}, status=status.HTTP_200_OK)


