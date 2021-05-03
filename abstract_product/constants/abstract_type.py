class AbstractType:
    AOP_PRODUCT = '1'
    FLAT_PRODUCT = '2'
    THANK_YOU_CARD = '3'


class VerboseAbstractType:
    AOP_PRODUCT = "aop_product"
    FLAT_PRODUCT = "flat_product"
    THANK_YOU_CARD = "thank_you_card"


ABSTRACT_TYPE_CHOICES = (
    (AbstractType.AOP_PRODUCT, VerboseAbstractType.AOP_PRODUCT),
    (AbstractType.FLAT_PRODUCT, VerboseAbstractType.FLAT_PRODUCT),
    (AbstractType.THANK_YOU_CARD, VerboseAbstractType.THANK_YOU_CARD)
)

PRODUCT_DESTROYABLE_TYPE = [AbstractType.THANK_YOU_CARD]

ABSTRACT_TYPE_VERBOSE_DICT = {verbose: enum for enum, verbose in ABSTRACT_TYPE_CHOICES}
ABSTRACT_TYPE_DICT = {enum: verbose for enum, verbose in ABSTRACT_TYPE_CHOICES}
