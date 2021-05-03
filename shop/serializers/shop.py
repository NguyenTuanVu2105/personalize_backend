from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, IntegerField, FloatField

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from shop.models import Shop
from shop.serializers import EcommerceSerializer
from system_metadata.models import CurrencyExchangeRate
from system_metadata.serializers import CurrencyExchangeRateSerializer

import logging
logger = logging.getLogger(__name__)

class GenericRelationShopSerializer(GenericRelationSerializer):
    ecommerce = EcommerceSerializer()

    class Meta(GenericRelationSerializer.Meta):
        model = Shop
        fields = ['ecommerce', 'id', 'type', 'name', 'currency', 'url', 'update_time']


class BriefShopSerializer(ModelSerializer):
    ecommerce = EcommerceSerializer()
    status = CharField(source="verbose_status")
    currency_info = serializers.SerializerMethodField()

    def get_currency_info(self, obj):
        return CurrencyExchangeRateSerializer(obj.currency).data

    class Meta:
        model = Shop
        fields = ['ecommerce', 'id', 'name', 'currency', 'currency_info', 'url', 'update_time', 'status']


class ShopDetailSerializer(BriefShopSerializer):
    class Meta:
        model = Shop
        fields = ['ecommerce', 'id', 'name', 'currency', 'url', 'update_time', 'email', 'status']


class ShopSerializer(BriefShopSerializer):
    currency_exchange_rate = FloatField(source='currency.rate')
    currency_precision = IntegerField(source='currency.precision')

    class Meta:
        model = Shop
        fields = ['ecommerce', 'id', 'name', 'currency', 'url', 'currency_exchange_rate', 'currency_precision', 'update_time', 'status']


class MerchantServiceShopSerializer(ShopSerializer):
    ecommerce = CharField()
    shopId = CharField(source="id")
    shopName = CharField(source="url")
    accessToken = CharField(source="access_token")
    locationId = IntegerField(source="location_id")
    
    class Meta(ShopSerializer.Meta):
        fields = ['shopId', 'ecommerce', 'shopName', 'url', 'accessToken', 'locationId']

