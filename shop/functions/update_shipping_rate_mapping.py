import hashlib
import logging

from shop.models import ShopShippingRateMapping
from shipping.models import ShippingRate

logger = logging.getLogger(__name__)


def update_shipping_rate_mapping(shop, shipping_zone_data):
    rates = []
    rate_ids = []
    for shipping_zone_data in shipping_zone_data:
        countries_list_str = "".join(shipping_zone_data["countries"])
        for rate in shipping_zone_data["rates"]:
            zone_hash = hashlib.new("sha256")
            zone_hash.update((countries_list_str + rate).encode('utf-8'))
            rate_id = zone_hash.hexdigest()
            rates.append({
                "id": rate_id,
                "countries": shipping_zone_data["countries"],
                "name": rate
            })
            logger.info(rate_id)
            rate_ids.append(rate_id)

    ShopShippingRateMapping.objects.filter(shop=shop).exclude(hash_id__in=rate_ids).delete()
    mappings = []
    default_shipping_rate = ShippingRate.objects.filter(is_default=True).first()
    for rate in rates:
        mappings.append(ShopShippingRateMapping.objects.get_or_create(
            shop=shop,
            hash_id=rate["id"],
            e_commerce_shipping_rate_name=rate["name"],
            defaults={
                'shipping_rate': default_shipping_rate,
                "countries": rate["countries"]
            })[0])
    return mappings
