class OrderTypes:
    SHOPIFY = "1"
    PRINTHOLO = "2"


class VerboseOrderTypes:
    SHOPIFY = "standard"
    PRINTHOLO = "sample"


ORDER_TYPE_CHOICES = [
    (OrderTypes.SHOPIFY, VerboseOrderTypes.SHOPIFY),
    (OrderTypes.PRINTHOLO, VerboseOrderTypes.PRINTHOLO),
]
