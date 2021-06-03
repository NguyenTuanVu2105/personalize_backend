from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import GenericViewSet
from order.models import OrderTracker
from order.serializers import OrderTrackerSerializer
from rest_framework.permissions import AllowAny

import logging
logger = logging.getLogger(__name__)

class OrderTrackerViewSet(GenericViewSet):
    queryset = OrderTracker.objects.all()
    serializer_class = OrderTrackerSerializer
    permission_classes = [AllowAny, ]

    @action(methods=['GET'], detail=False, url_path=r'(?P<tracking_code>[0-9A-Za-z]+)')
    def get_tracker(self, request, *args, **kwargs):
        tracking_code = kwargs['tracking_code']
        try:
            tracker = OrderTracker.objects.filter(tracking_code=tracking_code).first()
            payloads = tracker.payloads
            if 'data' in payloads:
                return Response(tracker.payloads)
            else:
                return Response({"success": True, "data": tracker.payloads})
        except Exception as e:
            logger.error(e)
            return Response({"success": False})



