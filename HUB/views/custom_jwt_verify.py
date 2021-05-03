import jwt
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext as _
from rest_framework import exceptions

from HUB.helpers.auth_helper import regenerateAccessToken
from HUB.settings import app_setting

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
import logging

logger = logging.getLogger(__name__)


class CustomJWTAuthen(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if user.is_lock:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            try:
                jwt_value = self.verify_and_regenerate_token(request)
                payload = jwt_decode_handler(jwt_value)
            except:
                msg = _('Signature has expired.')
                raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        user = self.authenticate_credentials(payload)
        return (user, jwt_value)

    """
        Clients should authenticate by passing the token key in the "Authorization"
        HTTP header, prepended with the string specified in the setting
        `JWT_AUTH_HEADER_PREFIX`. For example:

            Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
        """

    def verify_and_regenerate_token(self, request):
        refresh_token = self.get_refresh_token_val(request)
        token = regenerateAccessToken(refresh_token)
        if token is None:
            return None
        else:
            return token['token']

    def get_refresh_token_val(self, request):
        if request.META.get(app_setting.REFRESH_TOKEN_HEADER):
            return request.META.get(app_setting.REFRESH_TOKEN_HEADER)
        elif request.COOKIES.get(app_setting.REFRESH_TOKEN):
            return request.COOKIES.get(app_setting.REFRESH_TOKEN)
        else:
            return None
