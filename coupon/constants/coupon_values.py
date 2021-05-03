class DiscountTarget:
    PACK_PRODUCTION_COST = "pack_production_cost"
    PACK_SHIPPING_COST = "pack_shipping_cost"


class DiscountAttribute:
    MIN_COST_IN_USD = "min_cost_in_usd"
    DISCOUNT_VALUE = "discount_value"
    MAX_DISCOUNT_IN_USD = "max_discount_in_usd"


class DiscountAttributeDefaultValue:
    UNLIMITED_MIN_COST_IN_USD = 0
    DEFAULT_DISCOUNT_VALUE = 0
    UNLIMITED_MAX_DISCOUNT_IN_USD = -1


DEFAULT_DISCOUNT_VALUE_CONFIG = {
    DiscountTarget.PACK_PRODUCTION_COST: {
        DiscountAttribute.MIN_COST_IN_USD: DiscountAttributeDefaultValue.UNLIMITED_MIN_COST_IN_USD,
        DiscountAttribute.DISCOUNT_VALUE: DiscountAttributeDefaultValue.DEFAULT_DISCOUNT_VALUE,
        DiscountAttribute.MAX_DISCOUNT_IN_USD: DiscountAttributeDefaultValue.UNLIMITED_MAX_DISCOUNT_IN_USD,
    },
    DiscountTarget.PACK_SHIPPING_COST: {
        DiscountAttribute.MIN_COST_IN_USD: DiscountAttributeDefaultValue.UNLIMITED_MIN_COST_IN_USD,
        DiscountAttribute.DISCOUNT_VALUE: DiscountAttributeDefaultValue.DEFAULT_DISCOUNT_VALUE,
        DiscountAttribute.MAX_DISCOUNT_IN_USD: DiscountAttributeDefaultValue.UNLIMITED_MAX_DISCOUNT_IN_USD,
    }
}
