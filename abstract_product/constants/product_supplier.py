class ProductSupplier:
    FULFILLMENT = '1'


class VerboseProductSupplier:
    FULFILLMENT = 'fulfillment'


PRODUCT_SUPPLIER_CHOICES = (
    (ProductSupplier.FULFILLMENT, VerboseProductSupplier.FULFILLMENT),
)

SUPPLIER_DICT = {key: verbose for key, verbose in PRODUCT_SUPPLIER_CHOICES}

SUPPLIER_DICT_REVERSE = {verbose: key for key, verbose in PRODUCT_SUPPLIER_CHOICES}
