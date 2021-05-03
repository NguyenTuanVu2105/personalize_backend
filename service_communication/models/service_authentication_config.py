from django.contrib.postgres.fields import JSONField
from django.db import models

from service_communication.constants.authenticated_service import AUTHENTICATION_SERVICE_TYPES
from service_communication.constants.authentication_type import AUTHENTICATION_TYPES


class ServiceAuthenticationConfig(models.Model):
    service_name = models.CharField(primary_key=True, max_length=20, choices=AUTHENTICATION_SERVICE_TYPES)
    authentication_type = models.CharField(max_length=10, choices=AUTHENTICATION_TYPES, db_index=True)
    meta = JSONField(default={})

    class Meta:
        db_table = 'service_communication_authentication_config'
        ordering = ['service_name']
