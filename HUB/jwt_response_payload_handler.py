import logging
import os

from django.contrib.auth.models import Permission

logger = logging.getLogger(__name__)


def auth_response_data(user, jwt_token, refresh_token=None):
    return {
        'token': jwt_token,
        'refresh_token': refresh_token,
        'user_id': user.id,
        'email': user.email,
        'name': user.name,
        'timezone': user.settings.timezone,
        'avatar_url': user.avatar,
        'message_id': user.message_id
    }


def staff_auth_response_data(user, jwt_token, refresh_token):
    permissions = [permission.codename for permission in user.user_permissions.all()] if not user.is_superuser else [
        permission.codename for permission in Permission.objects.filter(content_type_id=0)]
    return {
        'token': jwt_token,
        'refresh_token': refresh_token,
        'user_id': user.id,
        'email': user.email,
        'name': user.name,
        'timezone': user.settings.timezone,
        'avatar_url': user.avatar,
        'permissions': permissions
    }


ADMIN_CLIENT_URLS_AS_STR = os.environ.get('ADMIN_CLIENT_URLS')
ADMIN_CLIENT_URLS = ADMIN_CLIENT_URLS_AS_STR.split(";") if ADMIN_CLIENT_URLS_AS_STR is not None else []


def jwt_response_payload_handler(jwt_token, refresh_token, user=None, request=None, origin=None):
    request_origin = request.headers.get('Origin', 'printholo')
    if request_origin in ADMIN_CLIENT_URLS or origin in ADMIN_CLIENT_URLS:
        data = staff_auth_response_data(user, jwt_token, refresh_token)
    else:
        data = auth_response_data(user, jwt_token, refresh_token)
    return data
