class ShopStatus:
    INACTIVE = '0'
    ACTIVE = '1'
    ERROR = '2'
    UNAUTH = '3'


class VerboseShopStatus:
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    ERROR = 'error'
    UNAUTH = 'unauth'

SHOP_STATUS_CHOICES = [
    (ShopStatus.INACTIVE, VerboseShopStatus.INACTIVE),
    (ShopStatus.ACTIVE, VerboseShopStatus.ACTIVE),
    (ShopStatus.ERROR, VerboseShopStatus.ERROR),
    (ShopStatus.UNAUTH, VerboseShopStatus.UNAUTH)
]

IGNORE_QUERY_STATUSES = [ShopStatus.UNAUTH, ShopStatus.ERROR]