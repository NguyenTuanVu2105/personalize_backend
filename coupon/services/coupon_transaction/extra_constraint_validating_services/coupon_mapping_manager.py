from coupon.constants.constraint_validating_types import ConstraintValidatingType
from .base import CouponExtraConstraintValidatingService
from .order_with_one_item_one_quantity_validating_service import OrderWithOneItemOneQuantityValidatingService


class CouponValidatorMappingManager:
    VALIDATOR_MAPPING = {
        ConstraintValidatingType.UNKNOWN: CouponExtraConstraintValidatingService,
        ConstraintValidatingType.ORDER_WITH_ONE_ITEM_ONE_QUANTITY: OrderWithOneItemOneQuantityValidatingService
    }

    @classmethod
    def get_service_cls(cls, constraint_validating_type):
        return cls.VALIDATOR_MAPPING.get(constraint_validating_type)
