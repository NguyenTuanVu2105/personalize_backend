import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from HUB.functions import get_client_ip
from HUB.viewsets.base import BaseMixin
from user.forms import ForgotPasswordForm
from user.tasks import send_forgot_password_task

User = get_user_model()

RECAPTCHA_SECRET_KEY = settings.RECAPTCHA_SECRET_KEY
VALIDATE_CAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

import logging

logger = logging.getLogger(__name__)


class ForgotPasswordView(BaseMixin, APIView):
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    error_messages = {}

    def post(self, request):
        request_data = request.data
        user_registration_form = ForgotPasswordForm(data=request_data)
        if user_registration_form.is_valid():
            validate_data = {
                'secret': RECAPTCHA_SECRET_KEY,
                'response': request_data['gRecaptcha'],
                'remoteip': get_client_ip(self.request),  # Optional
            }
            validate_request = requests.post(VALIDATE_CAPTCHA_URL, validate_data)
            user = User.objects.filter(email=request_data['email']).first()
            if validate_request.json()['success'] and user:
                try:
                    send_forgot_password_task.delay(user_id=user.id, user_email=request_data['email'])
                    logger.info(request_data['email'])
                except Exception as e:
                    return Response({"success": False, "message": str(e)})

                else:
                    response_data = {
                        "message": "Please check your email inbox to get the link for password resetting"
                    }
                    return Response({"success": True, "data": response_data})

            elif not user:
                return Response(data={"success": False, 'message': 'This email has been not registered'},
                                status=status.HTTP_200_OK)

            else:
                return Response(data={"success": False, 'message': 'ReCAPTCHA verification is failed.'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            errors = [error for error in user_registration_form.errors]
            return Response(data={"success": False, 'message': 'This fields is required:  {}'.format(errors)},
                            status=status.HTTP_200_OK)
