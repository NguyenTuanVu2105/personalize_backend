class DiscountType:
    MONETARY_CUT_DOWN_BY_VALUE = "1"  # discount [10$]: 30$ - 10$ -> 20$
    MONETARY_CUT_DOWN_TO_VALUE = "2"  # discount  [1$]: 30$ -> 1$
    PERCENTAGE_CUT_DOWN_BY_VALUE = "3"  # discount [50%]: 30$ - 30$ * 50% = 15$


class VerboseDiscountType:
    MONETARY_CUT_DOWN_BY_VALUE = "monetary_cut_down_by_value"
    MONETARY_CUT_DOWN_TO_VALUE = "monetary_cut_down_to_value"
    PERCENTAGE_CUT_DOWN_BY_VALUE = "percentage_cut_down_by_value"


DISCOUNT_TYPE_CHOICES = [
    (DiscountType.MONETARY_CUT_DOWN_BY_VALUE, VerboseDiscountType.MONETARY_CUT_DOWN_BY_VALUE),
    (DiscountType.MONETARY_CUT_DOWN_TO_VALUE, VerboseDiscountType.MONETARY_CUT_DOWN_TO_VALUE),
    (DiscountType.PERCENTAGE_CUT_DOWN_BY_VALUE, VerboseDiscountType.PERCENTAGE_CUT_DOWN_BY_VALUE),
]
