import logging

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions.permissions import HeaderBaseAuthentication
from HUB.viewsets.base import GenericViewSet
from order.models import Order
from order.serializers import OrderSerializer
from order.services.service_order import update_order, create_order
from service_communication.constants.authenticated_service import AuthenticatedService

logger = logging.getLogger(__name__)


class OrderServiceAdapterViewSet(mixins.CreateModelMixin,
                                 GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [HeaderBaseAuthentication]
    service_name = AuthenticatedService.ECOMMERCE_ADAPTER

    error_messages = {
        "order": {
            "invalid": "The order is invalid",
            "existed": "The order is existed",
        },
        "shop": {
            "invalid": "This shop is invalid",
        },
    }

    def create(self, request, *args, **kwargs):
        create_order(request.data)
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="update")
    def update_order_info(self, request):
        update_order(request.data)
        return Response({"success": True})
