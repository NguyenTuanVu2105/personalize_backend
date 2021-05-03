# from rest_framework.authtoken.models import Token
import requests
from django.utils.encoding import smart_text
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from HUB import settings


def string_to_boolean(value):
    if value is not None and value.lower() == 'false':
        return False
    else:
        return True


# def user_is_authenticated(token):
#     try:
#         token_object =  Token.objects.get(key=token)
#     except Token.DoesNotExist:
#         return False
#     else:
#         return True
#
# def get_user_from_token(token):
#     try:
#         token_object =  Token.objects.get(key=token)
#     except Token.DoesNotExist:
#         print('Token is invalid')
#         return None
#     else:
#         return token_object.user
def get_token_from_request(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'].lower()

    if not auth:
        if settings.JWT_AUTH['JWT_AUTH_COOKIE']:
            return request.COOKIES.get(settings.JWT_AUTH['JWT_AUTH_COOKIE'])
        return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = 'Invalid Authorization header. No credentials provided.'
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
        raise exceptions.AuthenticationFailed(msg)

    return auth[1]


def split_word(string):
    word = string.split(" ")
    return word


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_country_code(ip_address):
    res = ''
    if not ip_address:
        return res
    obtain_geolocation_api = 'http://ip-api.com/json/{ip_address}'
    try:
        geolocation = requests.get(obtain_geolocation_api.format(ip_address=ip_address)).json()
        res = geolocation.get('countryCode')
    except Exception as e:
        res = ''
    return res
