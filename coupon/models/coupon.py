from django.db import models
from django.contrib.postgres.fields import JSONField

from HUB.models.random_id_model import RandomIDModel
from coupon.constants.discount_types import DISCOUNT_TYPE_CHOICES
from coupon.constants.constraint_validating_types import CONSTRAINTS_VALIDATING_TYPE_CHOICES, ConstraintValidatingType
from coupon.managers.coupon import CouponManager
from order.models import Order
from coupon.constants.coupon_values import DEFAULT_DISCOUNT_VALUE_CONFIG
from .coupon_campaign import CouponCampaign


class Coupon(RandomIDModel):
    campaign = models.ForeignKey(CouponCampaign, on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='coupons')
    orders = models.ManyToManyField(to=Order, through="coupon.RedeemedCouponTransaction",
                                    related_name='applied_coupons')

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, null=False, blank=False)
    value_config = JSONField(default=DEFAULT_DISCOUNT_VALUE_CONFIG)
    code = models.CharField(max_length=30, unique=True)

    redeeming_limit = models.PositiveIntegerField()
    valid_until = models.DateTimeField(blank=True, null=True)
    constraint_validating_type = models.CharField(max_length=20, choices=CONSTRAINTS_VALIDATING_TYPE_CHOICES,
                                                  default=ConstraintValidatingType.UNKNOWN, blank=True)
    extra_constraints = JSONField(default=dict, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = CouponManager()

    class Meta:
        db_table = "coupon"
        ordering = ['id']

    def __str__(self):
        return self.code
