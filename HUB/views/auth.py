from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken

from HUB.helpers.auth_helper import createRefreshToken, revokeRefreshToken, regenerateAccessToken, get_refresh_token_val
from HUB.permissions import IsAuthenticated
from HUB.settings import app_setting
from HUB.viewsets.base import BaseGenericAPIView
from shop.functions import create_user_printholo_store

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def retrieve_common_response(user, serializer, request):
    if not user.is_lock:
        if user.is_email_confirmed:
            refresh_token = createRefreshToken(user.id)
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, refresh_token, user, request)
            response = Response(response_data)
            response[app_setting.REFRESH_TOKEN] = refresh_token
            create_user_printholo_store(user=user)
            return response
        else:
            return Response({"success": False,
                             "message": "You need active account before login. Please check mail to active account."},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"success": False,
                         "message": "Account is disabled. Please contact with our support to unlock."},
                        status=status.HTTP_400_BAD_REQUEST)


class JSONWebTokenAPIView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            return retrieve_common_response(user, serializer, request)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JSONStaffWebTokenAPIView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            if user.is_staff:
                return retrieve_common_response(user, serializer, request)
            else:
                return Response({"success": False,
                                 "message": "You do not have permission to perform this action."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RevokeJSONWebTokenAPIView(BaseGenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):

        try:
            refresh_token = get_refresh_token_val(request)
            isRevoke = revokeRefreshToken(refresh_token)
            if isRevoke:
                response = Response({'success': True, "message": "Logout success"})
                response[app_setting.REFRESH_TOKEN] = None
                request.auth = None
                cookieKeys = request.COOKIES.keys()
                if app_setting.REFRESH_TOKEN in cookieKeys:
                    response.delete_cookie(app_setting.REFRESH_TOKEN)
                if api_settings.JWT_AUTH_COOKIE in cookieKeys:
                    response.delete_cookie(api_settings.JWT_AUTH_COOKIE)
            else:
                response = Response({'success': False, "message": "Can not revoke token"})
            return response
        except:
            return Response({'success': False, "message": "Logout failed"})


class GetJSONWebTokenByRefreshAPIView(BaseGenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            response_data = regenerateAccessToken(refresh_token)
            if response_data is None:
                response = Response({"message": "Can not get access token"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response(response_data)
            return response
        except:
            return Response({"message": "Can not get access token"}, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class ObtainJSONStaffWebToken(JSONStaffWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
obtain_jwt_staff_token = ObtainJSONStaffWebToken.as_view()
obtain_jwt_token_logout = RevokeJSONWebTokenAPIView.as_view()
obtain_jwt_token_by_refresh_token = GetJSONWebTokenByRefreshAPIView.as_view()
