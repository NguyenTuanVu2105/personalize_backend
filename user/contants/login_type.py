class LoginType:
    WEB = '1'
    SHOPIFY = '2'


class VerboseLoginType:
    WEB = 'web'
    SHOPIFY = 'shopify'


LOGIN_TYPE_CHOICES = [
    (LoginType.WEB, VerboseLoginType.WEB),
    (LoginType.SHOPIFY, VerboseLoginType.SHOPIFY)
]
