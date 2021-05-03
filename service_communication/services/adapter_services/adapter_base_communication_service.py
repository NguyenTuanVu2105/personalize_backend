import logging

from django.conf import settings

from service_communication.services.abstract_service import AbstractCommunicationService

logger = logging.getLogger(__name__)


class AdapterBaseCommunicationService(AbstractCommunicationService):
    HOST = settings.SHOPIFY_ADAPTER_HOST
    ENDPOINTS = {

    }