from PIL import ImageFile
from django.contrib.auth import get_user_model

from system_metadata.constants import DEFAULT_CURRENCY
from user_product.models import UserVariant, UserVariantPrice

User = get_user_model()
ImageFile.LOAD_TRUNCATED_IMAGES = True
import logging

logger = logging.getLogger(__name__)


def create_user_variants(user_product, variants, artworks, shops):
    user_variants_to_create = []
    user_variants_to_update = []
    user_variant_prices_to_create = []
    valid_currencies = [DEFAULT_CURRENCY]

    for shop in shops:
        valid_currencies.append(shop['currency'])
    valid_currencies = list(set(valid_currencies))

    for sort_index, variant in enumerate(variants):
        abstract_variant_id = variant['abstract_variant']
        user_variants_to_create.append(UserVariant(user_product=user_product,
                                                   abstract_variant_id=abstract_variant_id,
                                                   sort_index=sort_index))

    created_user_variants = UserVariant.objects.bulk_create(user_variants_to_create)

    for index, variant in enumerate(variants):
        user_variant = created_user_variants[index]
        user_variant_id = user_variant.id
        user_variant.sku = user_variant_id
        user_variants_to_update.append(user_variant)

        for currency in variant['price']:
            if currency in valid_currencies:
                value = variant['price'][currency]['value']
                user_variant_prices_to_create.append(
                    UserVariantPrice(value=value, currency=currency, user_variant_id=user_variant_id))

    UserVariant.objects.bulk_update(user_variants_to_update, ['sku'])
    UserVariantPrice.objects.bulk_create(user_variant_prices_to_create)

    # Logged, 4 queries