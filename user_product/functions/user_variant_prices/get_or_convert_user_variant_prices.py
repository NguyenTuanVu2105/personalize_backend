import logging
import traceback

from django.contrib.auth import get_user_model

from system_metadata.models import CurrencyExchangeRate
from user_product.models import UserVariantPrice
from .round_price import round_price
User = get_user_model()

logger = logging.getLogger(__name__)


def get_or_convert_user_variant_prices(user_variants, destination_currency_key):
    try:
        result_dict = {}
        destination_user_variant_prices = UserVariantPrice.objects.only('user_variant_id', 'value').filter(
            user_variant__in=user_variants,
            currency=destination_currency_key)

        if len(destination_user_variant_prices) != len(user_variants):
            logger.info("{}. THIS CURRENCY IS NOT IN DATABASE!!!!".format(destination_currency_key))

            source_currency_key = UserVariantPrice.objects.only('currency').filter(
                user_variant=user_variants.first()).first().currency
            source_currency = CurrencyExchangeRate.objects.only('rate').get(currency=source_currency_key)
            destination_currency = CurrencyExchangeRate.objects.only('rate').get(currency=destination_currency_key)

            current_rate = destination_currency.rate / source_currency.rate
            destination_currency_precision = destination_currency.precision

            user_variant_prices_to_create = []
            for user_variant in user_variants:
                source_user_variant_price = UserVariantPrice.objects.only('value').get(user_variant=user_variant,
                                                                                       currency=source_currency_key)
                source_user_variant_price_value = source_user_variant_price.value
                destination_user_variant_price_value = round_price(source_user_variant_price_value * current_rate,
                                                                   destination_currency_precision)
                user_variant_price = UserVariantPrice(user_variant=user_variant, currency=destination_currency_key,
                                                      value=destination_user_variant_price_value)
                user_variant_prices_to_create.append(user_variant_price)

            user_variant_prices = UserVariantPrice.objects.bulk_create(user_variant_prices_to_create)

        else:
            logger.info("{}. THIS CURRENCY IS ALREADY IN DATABASE!!!!".format(destination_currency_key))
            user_variant_prices = destination_user_variant_prices

        for user_variant_price in user_variant_prices:
            result_dict.update({
                user_variant_price.user_variant_id: float(user_variant_price.value)
            })

        return result_dict

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
        raise e
