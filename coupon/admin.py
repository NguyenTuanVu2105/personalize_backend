from django.contrib import admin

from coupon.models import CouponCampaign, Coupon, RedeemedCouponTransaction


@admin.register(CouponCampaign)
class CouponCampaignAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "create_time", "create_time")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "id", "campaign", "name", "description", "discount_type", "value_config", "code", "redeeming_limit", "valid_until",
        "extra_constraints", "create_time", "update_time")


@admin.register(RedeemedCouponTransaction)
class RedeemedCouponTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "coupon", "idempotency_key", "redeemed_detail", "redeemed_time")
