from django_filters import FilterSet
from coupon.models import Coupon


class CouponFilter(FilterSet):
    class Meta:
        model = Coupon
        fields = ('campaign_id',)
