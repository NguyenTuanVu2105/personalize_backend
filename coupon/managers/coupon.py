from django.db.models import Manager, QuerySet, Count


class BaseCouponManager(Manager):
    def get_queryset(self):
        return super().get_queryset()


class CouponQueryset(QuerySet):
    def include_redeemed_count(self):
        return self.annotate(redeemed_count=Count("redeemed_coupon_transactions"))


CouponManager = BaseCouponManager.from_queryset(CouponQueryset)
