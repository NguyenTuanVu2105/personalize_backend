from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
import uuid
import warnings
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from calendar import timegm


def jwt_payload_handler(user, expired_time_delta=None):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )
    expired_time_delta = expired_time_delta or api_settings.JWT_EXPIRATION_DELTA
    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + expired_time_delta
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload
