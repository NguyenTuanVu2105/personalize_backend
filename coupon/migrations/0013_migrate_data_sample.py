import django.contrib.postgres.fields.jsonb
from django.db import migrations

from coupon.constants.constraint_validating_types import ConstraintValidatingType
from coupon.constants.discount_types import DiscountType
from coupon.models import CouponCampaign, Coupon


def migrate_coupon_data_sample(apps, schema_editor):
    coupon_campaign = CouponCampaign.objects.create(name="Default Campaign",
                                                    description="Coupon Campaign sampled from data migrations")
    Coupon.objects.create(campaign=coupon_campaign, name="AOP 1$",
                          description="All AOP product are discounted to 1$ on PrintHolo but 1$ (1 apply/user)",
                          discount_type=DiscountType.MONETARY_CUT_DOWN_TO_VALUE,
                          value_config={"pack_shipping_cost": {"discount_value": 0, "min_cost_in_usd": 0,
                                                               "max_discount_in_usd": -1},
                                        "pack_production_cost": {"discount_value": 1, "min_cost_in_usd": 0,
                                                                 "max_discount_in_usd": -1}},
                          code="AOP1D",
                          redeeming_limit=1000,
                          valid_until="2021-11-20 00:00:00",
                          constraint_validating_type=ConstraintValidatingType.ORDER_WITH_ONE_ITEM_ONE_QUANTITY,
                          extra_constraints={
                              "abstract_product_skus": ["AFM02", "AZH02", "ASS02", "AHD01", "AHD02", "ASS01", "ABJ01",
                                                        "APPC01", "AZH01", "ANG01", "ATS01", "AFM01"]})


class Migration(migrations.Migration):
    dependencies = [
        ('coupon', '0012_auto_20201120_1658'),
    ]

    operations = [
        migrations.RunPython(migrate_coupon_data_sample),
    ]
