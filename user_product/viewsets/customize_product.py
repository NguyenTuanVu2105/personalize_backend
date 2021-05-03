# from rest_framework.decorators import action
# from rest_framework.response import Response

# from HUB.viewsets.base import GenericViewSet
# from rest_framework.permissions import AllowAny
# from abstract_product.models.abstract_product import AbstractProduct
# from user_product.models.shop_user_product import ShopUserProduct 

# import logging
# logger = logging.getLogger(__name__)

# class CustomizeProductViewSet(GenericViewSet):
#     queryset = OrderTracker.objects.all()
#     serializer_class = OrderTrackerSerializer
#     permission_classes = [AllowAny, ]

#     @action(methods=['GET'], detail=False, url_path=r'(?P<tracking_code>[0-9A-Za-z]+)')
#     def get_tracker(self, request, *args, **kwargs):
#         tracking_code = kwargs['tracking_code']
#         try:
#             tracker = OrderTracker.objects.filter(tracking_code=tracking_code).first()
#             return Response(tracker.payloads)
#         except Exception as e:
#             logger.error(e)
#             return Response({"success": False})