import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from HUB.viewsets.base import BaseGenericAPIView
from user.contants import RESET_PASSWORD_RESPONSE_CODE, RESET_PASSWORD_RESPONSE_MESSAGE
from user.functions.email_token_generator import forgot_password_token

User = get_user_model()
import logging

logger = logging.getLogger(__name__)


class ResetPasswordView(BaseGenericAPIView):
    error_messages = {}
    permission_classes = [AllowAny, ]

    def post(self, request):
        try:
            request_data = request.data
            uidb64 = request_data['uid']
            token = request_data['token']
            password = request_data['password']
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"success": False, "data": {
                'message': RESET_PASSWORD_RESPONSE_MESSAGE.INVALID,
                'code': RESET_PASSWORD_RESPONSE_CODE.INVALID,
            }})
        except Exception as e:
            return Response({"success": False, "message": str(e)})
        else:
            if user is not None and forgot_password_token.check_token(user,
                                                                      token) and token == user.token_forgot_password:
                # activate user and login:
                import pytz
                utc = pytz.UTC
                now = datetime.datetime.now()
                now = utc.localize(now)
                cnow = now.replace(tzinfo=utc)
                response_data = {}

                if cnow > user.token_forgot_password_expire_time:
                    response_data.update({
                        'message': RESET_PASSWORD_RESPONSE_MESSAGE.EXPIRED,
                        'code': RESET_PASSWORD_RESPONSE_CODE.EXPIRED,
                    })
                    return Response({"success": False, "data": response_data})

                else:
                    user.set_password(password)
                    user.is_email_confirmed = True
                    user.last_change_password = timezone.now()
                    user.token_forgot_password = None
                    user.save()
                    response_data.update({
                        'message': RESET_PASSWORD_RESPONSE_MESSAGE.SUCCESS,
                        'code': RESET_PASSWORD_RESPONSE_CODE.SUCCESS,
                    })
                    return Response({"success": True, "data": response_data})

            else:
                return Response({"success": False, "data": {
                    'message': RESET_PASSWORD_RESPONSE_MESSAGE.INVALID,
                    'code': RESET_PASSWORD_RESPONSE_CODE.INVALID,
                }})
