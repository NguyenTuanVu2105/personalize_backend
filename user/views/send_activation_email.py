import traceback

import jwt
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from HUB.functions import get_token_from_request
from HUB.viewsets.base import BaseGenericAPIView
from user.functions.send_activation_email import send_activation_email

User = get_user_model()


class SendActivationEmail(BaseGenericAPIView):
    error_messages = {}

    def post(self, request):
        token = get_token_from_request(request)
        user_id = jwt.decode(token, None, None)['user_id']
        user = User.objects.get(pk=user_id)
        if user.is_email_confirmed:
            return Response({"success": False,
                             "message": "Your account have already been actived, so you don't need to active it again!"})
        else:
            try:
                send_activation_email(user_id)
            except Exception as e:
                traceback.print_exc()
                return Response({"success": False,
                                 "message": str(e)})
            else:
                return Response({"success": True,
                                 "message": "An activation email is sent to your email. Please open it and active your account!"})
