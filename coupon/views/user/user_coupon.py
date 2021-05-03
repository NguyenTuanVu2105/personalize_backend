import logging

from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from coupon.models import Coupon
from coupon.services.coupon_transaction.coupon_redeeming import redeem_coupon_by_user_request, cancel_coupon_by_user_request

logger = logging.getLogger(__name__)


class UserCouponViewSet(AuthenticatedGenericViewSet):
    queryset = Coupon.objects.none()

    @action(methods=["POST"], detail=False, url_path="redeem")
    def redeem_coupon_view(self, request):
        try:
            redeem_coupon_by_user_request(request.data, user=request.user)
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="cancel")
    def cancel_coupon_view(self, request):
        try:
            cancel_coupon_by_user_request(request.data, user=request.user)
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True})
