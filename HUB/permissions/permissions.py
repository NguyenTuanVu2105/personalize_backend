import logging
import re

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from service_communication.constants.authentication_type import AuthenticationType
from service_communication.hmac_utils import authenticate_request
from service_communication.hmac_utils.preprocessor import hmac_fulfill_preprocessor
from service_communication.models import ServiceAuthenticationConfig
from ..functions import get_client_ip

logger = logging.getLogger(__name__)

User = get_user_model()


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_seller())


class HasCustomPermission(BasePermission):
    def __init__(self, permissions):
        super().__init__()
        self.permissions = permissions

    def has_permission(self, request, view):
        return request.user.has_perms(self.permissions)

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(self.permissions)


class HeaderBaseAuthentication(BasePermission):
    def has_permission(self, request, view):
        try:
            config = ServiceAuthenticationConfig.objects.get(pk=view.service_name)
        except ServiceAuthenticationConfig.DoesNotExist:
            return True
        if config.authentication_type == AuthenticationType.HEADER:
            request_headers = request.headers
            required_headers = config.meta
            for header_name in required_headers:
                if request_headers.get(header_name, None) != required_headers[header_name]:
                    logger.info(request_headers)
                    logger.info(required_headers)
                    return False
            return True
        if config.authentication_type == AuthenticationType.IP:
            client_ip = get_client_ip(request)
            allow_ip_whitelist = config.meta.get("whitelist").split(";")
            for allowed_ip in allow_ip_whitelist:
                allowed_ip_reg = allowed_ip.replace('.', '\\.').replace('*', '\\d+')

                if re.match(allowed_ip_reg, client_ip):
                    return True
            logger.info(client_ip)
            return False
        if config.authentication_type == AuthenticationType.H_MAC:
            if not config.meta.get('enable', True):
                return True
            message, signature = hmac_fulfill_preprocessor.obtain_key_pair(request)
            authenticated = authenticate_request(message, signature, config.meta.get('secret_key'),
                                                 config.meta.get('algorithm'))
            debug = config.meta.get('debug', True)
            if not debug:
                return authenticated
            else:
                if not authenticated:
                    logger.exception(
                        f'HMAC request unauthenticated. Proof: {hmac_fulfill_preprocessor.obtain_header(request)}')
                return True
        return True
