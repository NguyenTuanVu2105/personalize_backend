class ShopLocationType:
    NOT_HAS_LOCATION = '0'
    WRONG_LOCATION = '1'

class ShopLocationVerboseType:
    NOT_HAS_LOCATION = 'not_has_location'
    WRONG_LOCATION = 'wrong_location'

SHOP_LOCATION_TYPE_CHOICES = [
    (ShopLocationType.NOT_HAS_LOCATION, ShopLocationVerboseType.NOT_HAS_LOCATION),
    (ShopLocationType.WRONG_LOCATION, ShopLocationVerboseType.WRONG_LOCATION)
]