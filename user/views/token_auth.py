from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from HUB.helpers.auth_helper import createRefreshToken
from HUB.jwt_response_payload_handler import auth_response_data
from HUB.viewsets.base import BaseGenericAPIView

User = get_user_model()


class TokenAuthView(BaseGenericAPIView):
    permission_classes = []

    def post(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = token.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        refresh_token = createRefreshToken(user.id)
        jwt_token = jwt_encode_handler(payload)
        token.delete()
        response_data = auth_response_data(user, jwt_token, refresh_token)
        return Response(response_data)
