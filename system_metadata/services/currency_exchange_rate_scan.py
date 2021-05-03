import json

import requests
from django.utils import timezone

from HUB import settings
from system_metadata.models import CurrencyExchangeRate


def update_all_currency_ex_rates():
    currencies = CurrencyExchangeRate.objects.all().order_by('update_time')[:10]
    for currency in currencies:
        update_currency_ex_rate(currency)


def update_currency_ex_rate(exchange_rate):
    query = f'{settings.BASE_CURRENCY}_{exchange_rate.currency}'
    res = requests.get(settings.CURRENCY_CONVERT_API.format(query))
    rate = json.loads(res.text)[query]
    exchange_rate.rate = rate
    exchange_rate.update_time = timezone.now()
    exchange_rate.save()
