from functools import partial

from django.contrib.contenttypes.models import ContentType

from .permissions import HasCustomPermission
import logging

logger = logging.getLogger(__name__)


def get_permissions(permission_list):
    try:
        permission_content_type = ContentType.objects.get(pk=0)
        permission_content_type_name = permission_content_type.app_label
        permission_prefix = permission_content_type_name + "."

        standard_permission_list = [permission_prefix + permission if
                                    not permission.startswith(permission_prefix) else permission for permission in
                                    permission_list]

        # logger.info("GETPERMISSIONS")
        # logger.info(permission_list)
        # logger.info(standard_permission_list)
        return [partial(HasCustomPermission, standard_permission_list), ]
    except Exception as e:
        logger.exception(e)
        return False
