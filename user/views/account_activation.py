import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from HUB.viewsets.base import BaseGenericAPIView
from user.contants import ACTIVATION_ACCOUNT_RESPONSE_MESSAGE, ACTIVATION_ACCOUNT_RESPONSE_CODE
from user.functions.email_token_generator import account_activation_token

User = get_user_model()

import logging
logger = logging.getLogger(__name__)


class AccountActivation(BaseGenericAPIView):
    error_messages = {}
    permission_classes = [AllowAny, ]

    def post(self, request):
        try:
            request_data = request.data
            uidb64 = request_data['uid']
            token = request_data['token']
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"success": False, "data": {
                'message': ACTIVATION_ACCOUNT_RESPONSE_MESSAGE.INVALID,
                'code': ACTIVATION_ACCOUNT_RESPONSE_CODE.INVALID,
            }})
        except Exception as e:
            return Response({"success": False, "message": str(e)})
        else:
            if user is not None and account_activation_token.check_token(user,
                                                                         token) and user.token_confirmation == token:
                # activate user and login:
                import pytz
                utc = pytz.UTC
                now = datetime.datetime.now()
                now = utc.localize(now)
                cnow = now.replace(tzinfo=utc)
                response_data = {}

                if cnow > user.token_confirmation_expire_time:
                    response_data.update({
                        'message': ACTIVATION_ACCOUNT_RESPONSE_MESSAGE.EXPIRED,
                        'code': ACTIVATION_ACCOUNT_RESPONSE_CODE.EXPIRED,
                    })
                    return Response({"success": False, "data": response_data})

                elif user.is_email_confirmed:
                    response_data.update({
                        'message': ACTIVATION_ACCOUNT_RESPONSE_MESSAGE.ALREADY_ACTIVATED,
                        'code': ACTIVATION_ACCOUNT_RESPONSE_CODE.ALREADY_ACTIVATED,
                    })
                    return Response({"success": False, "data": response_data})

                else:
                    user.is_email_confirmed = True
                    user.save()
                    response_data.update({
                        'message': ACTIVATION_ACCOUNT_RESPONSE_MESSAGE.SUCCESS,
                        'code': ACTIVATION_ACCOUNT_RESPONSE_CODE.SUCCESS,
                    })
                    return Response({"success": True, "data": response_data})

            else:
                return Response({"success": False, "data": {
                    'message': ACTIVATION_ACCOUNT_RESPONSE_MESSAGE.INVALID,
                    'code': ACTIVATION_ACCOUNT_RESPONSE_CODE.INVALID,
                }})