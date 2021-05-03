import logging
from datetime import datetime

import pytz

logger = logging.getLogger(__name__)
BASE_TIME = datetime(2020, 12, 29, 5, 0, 0, 0, tzinfo=pytz.UTC)


def update_user_product_generate_fusion(user_product):
    updated_fusion_amount = 0
    for user_product_artwork_fusion in user_product.artwork_set.all():
        artwork_fusion_time = user_product_artwork_fusion.artwork_fusion.last_fusion_update_time
        if artwork_fusion_time and artwork_fusion_time > BASE_TIME:
            updated_fusion_amount = updated_fusion_amount + 1

    if user_product.combine_fusion:
        additional_fusion = len(user_product.additional_fusion_sides) if user_product.additional_fusion_sides else 0
        real_fusion_amount = additional_fusion + 1
        user_product_artwork_fusion = user_product.artwork_set.send_to_fulfill_filter().first()
        artwork_fusion = user_product_artwork_fusion.artwork_fusion
        user_product.is_updated_fusions = bool(
            artwork_fusion.last_fusion_update_time and artwork_fusion.last_fusion_update_time > BASE_TIME
            and real_fusion_amount == updated_fusion_amount)
        user_product.save()
    else:
        side_amount = len(user_product.abstract_product.sides.all())
        user_product.is_updated_fusions = bool(side_amount == updated_fusion_amount)
        user_product.save()