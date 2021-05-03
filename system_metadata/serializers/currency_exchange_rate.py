from rest_framework.serializers import ModelSerializer

from system_metadata.models import CurrencyExchangeRate


class CurrencyExchangeRateSerializer(ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['currency', 'rate', 'precision']


class BriefCurrencyExchangeRateSerializer(ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['currency']
