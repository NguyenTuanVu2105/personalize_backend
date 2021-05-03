import logging
import random
import string
from datetime import datetime

import jwt
from django.db.models import Q
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings

from HUB.jwt_response_payload_handler import auth_response_data
from HUB.settings import app_setting
from user.contants.login_type import LoginType
from user.models import User
from user.models.auth_token import AuthToken

logger = logging.getLogger(__name__)


def generateRandomString(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def createRefreshToken(userId, shopify_login=False):
    try:
        expiredTime = datetime.utcnow() + app_setting.REFRESH_TOKEN_EXPIRED
        payload = {
            "user_id": userId,
            "exp": expiredTime
        }
        refreshToken = jwt.encode(payload, app_setting.REFRESH_TOKEN_SECRET_KEY).decode('UTF-8')
        authModel = AuthToken()
        authModel.token = refreshToken
        authModel.user_id = userId
        authModel.type = LoginType.WEB if shopify_login else LoginType.SHOPIFY
        authModel.is_revoked = False

        authModel.save()
        return refreshToken
    except Exception as e:
        logger.exception(e)
        return None


def jwt_payload_refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, app_setting.REFRESH_TOKEN_SECRET_KEY)
        if verify_refresh_token_payload(payload):
            return payload
        return None
    except Exception as e:
        #logger.exception(e)
        return None


def revokeRefreshToken(token):
    try:
        payload_refresh_token = jwt_payload_refresh_token(token)
        authModel = AuthToken.objects.filter(token=token, user_id=payload_refresh_token['user_id'])
        authModel.update(
            is_revoked=True
        )
        return True
    except Exception as e:
        logger.exception(e)
        return False


def regenerateAccessToken(refresh_token):
    try:
        payload_refresh_token = jwt_payload_refresh_token(refresh_token)
        if payload_refresh_token:
            user_id = payload_refresh_token['user_id']
            user = User.objects.get(pk=user_id)
            if not user.is_lock:
                auth_model = AuthToken.objects.filter(token=refresh_token, user_id=payload_refresh_token['user_id'],
                                                      is_revoked=False).first()
                if auth_model:
                    auth_model.last_used_time = datetime.utcnow()
                    auth_model.save()
                    user = User.objects.get(id=payload_refresh_token['user_id'])
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response_data = {
                        'token': token
                    }
                    return response_data
                else:
                    return None
            return None
        return None
    except Exception as e:
        #logger.exception(e)
        return None


def get_refresh_token_val(request):
    if request.COOKIES.get(app_setting.REFRESH_TOKEN):
        return request.COOKIES.get(app_setting.REFRESH_TOKEN)
    elif request.META.get(app_setting.REFRESH_TOKEN_HEADER):
        return request.META.get(app_setting.REFRESH_TOKEN_HEADER)
    else:
        return None


def verify_refresh_token_payload(payload):
    try:
        currentTime = datetime.timestamp(datetime.utcnow())
        expiredTime = payload['exp']
        if expiredTime >= currentTime:
            return True
        return False
    except Exception as e:
        #logger.exception(e)
        return False


def clean_refresh_token_in_db():
    try:
        AuthToken.objects.filter(
            Q(is_revoked=True) | Q(create_time__lt=datetime.utcnow() - app_setting.REFRESH_TOKEN_EXPIRED) | Q(
                type=LoginType.SHOPIFY,
                last_used_time__lt=datetime.utcnow() - app_setting.SHOPIFY_REFRESH_TOKEN_MAX_EXPIRED)).delete()
        return True
    except Exception as e:
        logger.exception(e)
        return False


def retrieve_jwt_payload(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    refresh_token = createRefreshToken(user.id, shopify_login=True)
    response = auth_response_data(user, token, refresh_token)
    return response

# def retrieve_jwt_payload_without_refresh(user):
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     payload = jwt_payload_handler(user, expired_time_delta=app_setting.SHOPIFY_ACCESS_TOKEN_EXPIRED)
#     token = jwt_encode_handler(payload)
#     response = auth_response_data(user, token)
#     return response
