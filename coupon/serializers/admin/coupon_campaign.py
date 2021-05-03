from rest_framework.serializers import ModelSerializer

from coupon.models import CouponCampaign


class AdminCouponCampaignSerializer(ModelSerializer):
    class Meta:
        model = CouponCampaign
        fields = ("id", "name", "description", "create_time", "update_time")
