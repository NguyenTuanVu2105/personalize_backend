from rest_framework.serializers import ModelSerializer

from coupon.models import RedeemedCouponTransaction
from coupon.serializers.admin import AdminCouponSerializer
from user.serializers.user import BriefUserSerializer


class AdminRedeemedCouponTransactionSerializer(ModelSerializer):
    coupon = AdminCouponSerializer()
    user = BriefUserSerializer()

    class Meta:
        model = RedeemedCouponTransaction
        fields = ("id", "user", "order_id", "coupon")
