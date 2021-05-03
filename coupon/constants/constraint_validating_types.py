class ConstraintValidatingType:
    UNKNOWN = "0"
    ORDER_WITH_ONE_ITEM_ONE_QUANTITY = "1"


class VerboseConstraintValidatingType:
    UNKNOWN = "unknown"
    ORDER_WITH_ONE_ITEM_ONE_QUANTITY = "order_with_one_item_one_quantity"


CONSTRAINTS_VALIDATING_TYPE_CHOICES = (
    (ConstraintValidatingType.UNKNOWN, VerboseConstraintValidatingType.UNKNOWN),
    (ConstraintValidatingType.ORDER_WITH_ONE_ITEM_ONE_QUANTITY,
     VerboseConstraintValidatingType.ORDER_WITH_ONE_ITEM_ONE_QUANTITY)
)
