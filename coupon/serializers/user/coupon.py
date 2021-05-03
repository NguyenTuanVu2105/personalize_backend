from rest_framework.serializers import ModelSerializer

from coupon.models import Coupon


class UserBriefCouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("id", "name", "code")
