from django.contrib.auth import get_user_model

from abstract_product.models import AbstractProductVariant
from user_product.functions import create_user_product_from_ecomerce_product
from user_product.models import UserVariant, UserVariantPrice

User = get_user_model()
import logging

logger = logging.getLogger(__name__)


def create_user_mapping_variant(ecomerce_variant, abstract_variant_id, artworks, user_id):
    ecommerce_product = ecomerce_variant.ecommerce_product
    user_product = ecommerce_product.user_product_mapping
    if user_product is None:
        user_product = create_user_product_from_ecomerce_product(ecommerce_product, user_id)
    abstract_variant = AbstractProductVariant.objects.get(id=abstract_variant_id)
    user_variant = UserVariant.objects.create(user_product=user_product,
                                              sku=ecomerce_variant.sku,
                                              abstract_variant=abstract_variant
                                              )
    user_variant.save()
    currency = ecommerce_product.shop.currency
    value = ecomerce_variant.variant_meta['price']
    UserVariantPrice.objects.create(value=value, currency=currency.currency, user_variant=user_variant)
    ecomerce_variant.user_variant_mapping = user_variant
    ecomerce_variant.save()
    return user_variant
