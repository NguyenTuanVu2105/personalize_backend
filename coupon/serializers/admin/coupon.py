from coupon.serializers.user.coupon import UserBriefCouponSerializer


class AdminBriefCouponSerializer(UserBriefCouponSerializer):
    class Meta(UserBriefCouponSerializer.Meta):
        fields = ("id", "name", "description", "discount_type", "value_config", "code", "redeeming_limit", "valid_until", "extra_constraints", "constraint_validating_type")


class AdminCouponSerializer(AdminBriefCouponSerializer):
    class Meta(AdminBriefCouponSerializer.Meta):
        fields = (
            "id", "campaign_id", "name", "description", "discount_type", "value_config", "code", "redeeming_limit",
            "valid_until", "extra_constraints", "constraint_validating_type")
