from django.db.models import CharField

from HUB.models.random_id_model import RandomIDModel
from abstract_product.constants import PRODUCT_SUPPLIER_CHOICES, SUPPLIER_DICT


class FFMProductInfo(RandomIDModel):
    supplier = CharField(max_length=1, choices=PRODUCT_SUPPLIER_CHOICES)
    ph_product_sku = CharField(max_length=255)
    supplier_product_sku = CharField(max_length=255)

    class Meta:
        ordering = ['id']
        db_table = 'ffm_product_info'

    @property
    def verbose_supplier(self):
        return SUPPLIER_DICT[self.supplier]
