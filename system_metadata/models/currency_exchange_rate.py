from django.db import models
from django.utils.translation import gettext as _


class CurrencyExchangeRate(models.Model):
    currency = models.CharField(max_length=5, primary_key=True)
    rate = models.DecimalField(max_digits=32, decimal_places=10)
    precision = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'system_meta_currency_exchange_rate'
        ordering = ['currency']
        verbose_name = _('Currency Exchange Rate')
        verbose_name_plural = _('Currency Exchange Rates')

    def __str__(self):
        return self.currency
