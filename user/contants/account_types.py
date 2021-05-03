class AccountType:
    EMAIL = '1'
    GOOGLE = '2'
    SHOPIFY = '3'


class VerboseAccountType:
    EMAIL = 'email'
    GOOGLE = 'google'
    SHOPIFY = 'shopify'


ACCOUNT_TYPE_CHOICES = [
    (AccountType.EMAIL, VerboseAccountType.EMAIL),
    (AccountType.GOOGLE, VerboseAccountType.GOOGLE),
    (AccountType.SHOPIFY, VerboseAccountType.SHOPIFY)
]
