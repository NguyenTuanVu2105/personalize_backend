from system_metadata.models import CurrencyExchangeRate


def get_currency_rate(currency):
    return CurrencyExchangeRate.objects.get(currency=currency).rate


def convert_local_money_to_usd(amount, currency):
    rate = get_currency_rate(currency)
    return amount / rate


def convert_usd_to_local_money(amount, currency):
    rate = get_currency_rate(currency)
    return amount * rate
