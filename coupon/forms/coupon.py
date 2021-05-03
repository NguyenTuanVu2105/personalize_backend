from HUB.forms.base import PreserveNotNoneDataValueModelForm
from coupon.models import Coupon


class CouponForm(PreserveNotNoneDataValueModelForm):
    class Meta:
        model = Coupon
        fields = ["campaign", "name", "description", "discount_type", "value_config", "code", "redeeming_limit",
                  "valid_until", "extra_constraints", "constraint_validating_type"]
