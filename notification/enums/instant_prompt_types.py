class InstantPromptType:
    ADD_SHOP = "0"
    ADD_PAYMENT_METHOD = "1"
    BILLING_CHARGE_FAILED = "2"
    SHOW_TOUR_NEW_PRODUCT_DESIGN = "3"
    SHOW_TOUR_NEW_PRODUCT_PRICING = "4"
    SHOW_TOUR_PAYMENT_MANAGER = "5"
    SHOW_SHOP_SETTING = "6"
    TICKET_UNREAD = "7"
    SHOW_INTRODUCTION = "8"
    ORDER_PROCESSING_TIME = "9"
    POLICY_AGREEMENT = "10"


class VerboseInstantPromptType:
    ADD_SHOP = "add_shop"
    ADD_PAYMENT_METHOD = "add_payment_method"
    BILLING_CHARGE_FAILED = "billing_charge_failed"
    SHOW_TOUR_NEW_PRODUCT_DESIGN = "show_tour_new_product_design"
    SHOW_TOUR_NEW_PRODUCT_PRICING = "show_tour_new_product_pricing"
    SHOW_TOUR_PAYMENT_MANAGER = "show_tour_payment_manager"
    SHOW_SHOP_SETTING = "show_shop_setting"
    TICKET_UNREAD = "ticket_unread"
    SHOW_INTRODUCTION = "show_introduction"
    ORDER_PROCESSING_TIME = "order_processing_time"
    POLICY_AGREEMENT = "policy_agreement"


INSTANT_PROMPT_TYPES = [
    (InstantPromptType.ADD_SHOP, VerboseInstantPromptType.ADD_SHOP),
    (InstantPromptType.ADD_PAYMENT_METHOD, VerboseInstantPromptType.ADD_PAYMENT_METHOD),
    (InstantPromptType.BILLING_CHARGE_FAILED, VerboseInstantPromptType.BILLING_CHARGE_FAILED),
    (InstantPromptType.SHOW_TOUR_NEW_PRODUCT_DESIGN, VerboseInstantPromptType.SHOW_TOUR_NEW_PRODUCT_DESIGN),
    (InstantPromptType.SHOW_TOUR_NEW_PRODUCT_PRICING, VerboseInstantPromptType.SHOW_TOUR_NEW_PRODUCT_PRICING),
    (InstantPromptType.SHOW_TOUR_PAYMENT_MANAGER, VerboseInstantPromptType.SHOW_TOUR_PAYMENT_MANAGER),
    (InstantPromptType.SHOW_SHOP_SETTING, VerboseInstantPromptType.SHOW_SHOP_SETTING),
    (InstantPromptType.TICKET_UNREAD, VerboseInstantPromptType.TICKET_UNREAD),
    (InstantPromptType.SHOW_INTRODUCTION, VerboseInstantPromptType.SHOW_INTRODUCTION),
    (InstantPromptType.ORDER_PROCESSING_TIME, VerboseInstantPromptType.ORDER_PROCESSING_TIME),
    (InstantPromptType.POLICY_AGREEMENT, VerboseInstantPromptType.POLICY_AGREEMENT)

]

INSTANT_PROMPT_TYPE_VERBOSE_DICT = {verbose: status for status, verbose in INSTANT_PROMPT_TYPES}
INSTANT_PROMPT_TYPE_DICT = {status: verbose for status, verbose in INSTANT_PROMPT_TYPES}
