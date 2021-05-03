from rest_framework import mixins
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from coupon.models import RedeemedCouponTransaction, Coupon
from coupon.serializers.admin.redeemed_coupon_transaction import AdminRedeemedCouponTransactionSerializer


class AdminRedeemedCouponTransactionViewSet(SearchableListModelMixin,
                                 mixins.CreateModelMixin,
                                 AdminGenericViewSet):
    queryset = RedeemedCouponTransaction.objects.all()
    serializer_class = AdminRedeemedCouponTransactionSerializer

    @method_permission_required(get_permissions(['admin_coupon_view', ]))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_coupon_view', ]))
    def create(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request_data["user_id"]
        idempotency_key = user_id
        coupon = Coupon.objects.filter(code=request_data["code"]).first()
        RedeemedCouponTransaction.objects.create(user_id=user_id, coupon=coupon, idempotency_key=idempotency_key,
                                                 redeemed_detail={})
        return Response({"success": True})
