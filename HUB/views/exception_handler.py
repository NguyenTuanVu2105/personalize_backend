import logging

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404
from jwt import PyJWTError
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404) or isinstance(exc, ObjectDoesNotExist):
        return Response({"success": False, "message": "NOT_FOUND"}, status=404)
    elif isinstance(exc, PermissionDenied):
        return Response({"success": False, "message": "FORBIDDEN"}, status=403)
    elif isinstance(exc, PyJWTError):
        return Response({"success": False, "message": "UNAUTHORIZED"}, status=401)
    elif isinstance(exc, APIException):
        return Response({"success": False, "message": exc.detail}, status=exc.status_code)

    elif isinstance(exc, FormValidationError):
        if hasattr(context['view'], "error_messages"):
            error_messages = context['view'].error_messages
            field = exc.field
            code = exc.code
            if field in error_messages and code in error_messages[field]:
                return Response({"success": False, "message": error_messages[field][code]}, status=400)
            else:
                logger.info(field + " " + code)

    logger.exception(exc)
    return Response({"success": False}, status=400)
