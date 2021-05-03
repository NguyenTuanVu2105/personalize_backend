from django.conf import settings
from rest_framework_jwt.settings import api_settings
from HUB.settings import ACCESS_TOKEN_HEADER, app_setting


class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = settings.FRONTEND_SERVER_URL

        return response


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            jwt_value = request.auth
        except:
            jwt_value= None
        if jwt_value:
            # response.set_cookie(key=api_settings.JWT_AUTH_COOKIE, value=jwt_value,httponly=True, secure=app_setting.COOKIE_SECURE)
            response[ACCESS_TOKEN_HEADER] = jwt_value
        return response
