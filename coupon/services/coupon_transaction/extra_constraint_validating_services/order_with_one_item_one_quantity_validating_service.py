from django.core.exceptions import ValidationError

from .base import CouponExtraConstraintValidatingService


class OrderWithOneItemOneQuantityValidatingService(CouponExtraConstraintValidatingService):
    def verify(self):
        self.validate_basic_order_rules()
        self.validate_extra_order_rules()

    def validate_basic_order_rules(self):
        order_obj = self.order
        order_item_objs = order_obj.items.all()
        if len(order_item_objs) != 1:
            raise ValidationError(code="order", message="Order must have only one item")

        order_item_obj = order_item_objs[0]
        if order_item_obj.quantity != 1:
            raise ValidationError(code="order", message="Order item quantity must equal 1")

    def validate_extra_order_rules(self):
        extra_constraints = self.coupon.extra_constraints

        applicable_abstract_product_skus = set(extra_constraints.get("abstract_product_skus", []))
        order_abstract_product_skus = set(
            self.order.items.values_list("user_variant__user_product__abstract_product__sku", flat=True).distinct())
        if not order_abstract_product_skus.issubset(applicable_abstract_product_skus):
            raise ValidationError(code="order", message="Relating products are not valid with this coupon")
