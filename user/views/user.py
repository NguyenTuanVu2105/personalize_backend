import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from HUB.functions import get_client_ip
from HUB.viewsets.base import BaseMixin
from notification.services.instant_prompt import generate_default_instant_prompt
from shop.functions import create_user_printholo_store
from user.forms.user_registration import UserRegistrationForm
from user.functions import send_activation_email
from user.tasks import send_activation_email_task, update_geolocation_task, send_welcome_user_email_task

User = get_user_model()

RECAPTCHA_SECRET_KEY = settings.RECAPTCHA_SECRET_KEY
VALIDATE_CAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

import logging

logger = logging.getLogger(__name__)


def retrieveDefaultAvatarUrl(username):
    return "https://ui-avatars.com/api/?name=${}".format("+".join(username.split(' ')))


class CreateUserView(BaseMixin, APIView):
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    error_messages = {}

    def post(self, request):
        request_data = request.data
        user_registration_form = UserRegistrationForm(data=request_data)
        request_ip = get_client_ip(self.request)
        if user_registration_form.is_valid():
            # validate_data = {
            #     'secret': RECAPTCHA_SECRET_KEY,
            #     'response': request_data['gRecaptcha'],
            #     'remoteip': request_ip,  # Optional
            # }
            # validate_request = requests.post(VALIDATE_CAPTCHA_URL, validate_data)
            # logger.info('VALIDATE CAPTCHA...')
            # if validate_request.json()['success']:
            try:
                group = Group.objects.filter(name__contains='seller').first()
                user, created = User.objects.get_or_create(
                    email=request_data['email'],
                    name=request_data['name'],
                    group=group,
                    avatar=retrieveDefaultAvatarUrl(request_data['name']),
                    is_email_confirmed=False,
                )
                user.set_password(request_data['password'])
                user.save()

                if created:
                    send_welcome_user_email_task.delay(user_id=user.id)
                    send_activation_email_task.delay(user_id=user.id)
                    update_geolocation_task.delay(user_id=user.id, ip_address=request_ip)
                    generate_default_instant_prompt(user.id)   
                else:
                    return Response({"success": False, "message": "This email have been registered"})

            except Exception as e:
                return Response({"success": False, "message": str(e)})

            else:
                user_info = {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                }

                # get_or_create Printholo Store
                create_user_printholo_store(user=user)

                return Response({"success": True, "data": user_info})

            # else:
            #     logger.info('VALIDATE CAPTCHA FAILED')
            #     return Response(data={"success": False, 'message': 'ReCAPTCHA verification is failed.'},
            #                     status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            errors = [error for error in user_registration_form.errors]
            return Response(data={"success": False, 'message': 'This fields is required:  {}'.format(errors)},
                            status=status.HTTP_200_OK)
