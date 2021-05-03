from coupon.constants.constraint_validating_types import CONSTRAINTS_VALIDATING_TYPE_CHOICES
from helper.choice_helpers import find_verbose_type_from_choices


class CouponExtraConstraintValidatingService:
    def __init__(self, user, coupon, order):
        self.user = user
        self.coupon = coupon
        self.order = order

    def verify(self):
        verbose_type = find_verbose_type_from_choices(CONSTRAINTS_VALIDATING_TYPE_CHOICES,
                                                      self.coupon.constraint_validating_type)
        raise NotImplementedError(
            "Coupon with constraint_validating_type=[{}] was not implemented".format(verbose_type))
