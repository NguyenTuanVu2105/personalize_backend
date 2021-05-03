from django.contrib import admin

from system_metadata.models import CurrencyExchangeRate
from shipping.models import ShippingRate


@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'precision', 'create_time', 'update_time')

