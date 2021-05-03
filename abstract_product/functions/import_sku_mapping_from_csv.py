from abstract_product.constants import SUPPLIER_DICT_REVERSE
from abstract_product.models.ffm_product_infos import FFMProductInfo

import logging


def import_sku_mapping_form_csv(csv_reader):
    logger = logging.getLogger(__name__)
    num_existed = 0
    num_new_created = 0
    num_invalid = 0
    for index, row in list(enumerate(csv_reader))[1:]:
        supplier = SUPPLIER_DICT_REVERSE.get(row[0])
        ph_product_sku = row[1]
        ffm_product_sku = row[2]
        try:
            product_info, created = FFMProductInfo.objects.update_or_create(ph_product_sku=ph_product_sku,
                                                                            supplier=supplier,
                                                                            defaults={
                                                                                'supplier_product_sku': ffm_product_sku})
            if created:
                num_new_created += 1
            else:
                num_existed += 1
        except Exception as e:
            logger.exception(e)
            num_invalid += 1
    return num_new_created, num_existed, num_invalid
