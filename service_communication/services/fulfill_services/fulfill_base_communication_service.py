import logging

from django.conf import settings

from service_communication.services.abstract_service import AbstractCommunicationService

logger = logging.getLogger(__name__)


class FulfillBaseCommunicationService(AbstractCommunicationService):
    HOST = settings.FULFILLMENT_HOST
    ENDPOINTS = {

    }

    HEADERS = {"Authorization": f'Bearer {settings.FULFILLMENT_API_KEY}'}
