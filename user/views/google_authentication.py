import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from HUB.functions import get_client_ip
from HUB.helpers.auth_helper import createRefreshToken
from HUB.jwt_response_payload_handler import auth_response_data
from HUB.settings import app_setting
from HUB.viewsets.base import BaseGenericAPIView
from notification.services.instant_prompt import generate_default_instant_prompt
from shop.functions import create_user_printholo_store
from user.contants import AccountType
from user.forms import GAuthenticationForm
from user.tasks import update_geolocation_task, send_welcome_user_email_task

User = get_user_model()

logger = logging.getLogger(__name__)


class GoogleAuthView(BaseGenericAPIView):
    """
    Post call for user login.
    """
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]

    def post(self, request, format=None):
        request_data = request.data
        form = GAuthenticationForm(data=request_data)
        group = Group.objects.filter(name__contains='seller').first()
        admin_group = Group.objects.filter(name__contains='admin').first()

        if form.is_valid():
            try:
                idinfo = id_token.verify_oauth2_token(request_data['id_token'], requests.Request(),
                                                      settings.GOOGLE_CLIENT_ID)
                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    return Response(ValueError('Wrong issuer.'))
                email = idinfo['email']
                name = idinfo['name']
                avatar = idinfo['picture']
                user, created = User.objects.get_or_create(email=email)

                if created:
                    user.name = name
                    user.avatar = avatar
                    user.account_type = AccountType.GOOGLE
                    user.set_password("")
                    user.is_email_confirmed = True
                    send_welcome_user_email_task.delay(user_id=user.id)
                    generate_default_instant_prompt(user.id)
                if user.group != admin_group:
                    user.group = group
                # if not user.is_email_confirmed and not user.is_lock:
                #     send_warning_authenication_task.delay(user_id=user.id)
                user.save()
                if user.is_lock:
                    return Response({"success": False, "message": "User is disabled"})
                if created:
                    update_geolocation_task.delay(user_id=user.id, ip_address=get_client_ip(self.request))
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                refresh_token = createRefreshToken(user.id)
                response_data = auth_response_data(user, token, refresh_token)
                response = Response(response_data, status=status.HTTP_200_OK)
                # response header refresh_token:
                response[app_setting.REFRESH_TOKEN] = refresh_token
                # expiration = (datetime.utcnow() +
                #               app_setting.REFRESH_TOKEN_EXPIRED)
                # response.set_cookie(key=app_setting.REFRESH_TOKEN,
                #                     value=refresh_token,
                #                     httponly=True,
                #                     samesite='Lax',
                #                     secure=app_setting.COOKIE_SECURE,
                #                     expires=expiration
                #                     )
                # if api_settings.JWT_AUTH_COOKIE:
                #     expiration = (datetime.utcnow() +
                #                   api_settings.JWT_EXPIRATION_TIME_IN_MINUTE)
                #     response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                #                         token,
                #                         expires=expiration,
                #                         httponly=True,
                #                         secure=app_setting.COOKIE_SECURE
                #                         )

                # get_or_create Printholo Store
                create_user_printholo_store(user=user)

                return response

            except ValueError:
                # Invalid token
                return Response({"success": False, "message": "Invalid Token"})
            except Exception as e:
                logger.info(e)
                return Response({"success": False, "message": "Exception"})
        else:
            return Response(ValidationError(code="G-Auth", message=form.errors), status=status.HTTP_400_BAD_REQUEST)
