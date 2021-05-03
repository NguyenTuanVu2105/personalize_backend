from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from order.models.order_invallid import OrderInvalid
from shop.serializers.shop import BriefShopSerializer


class OrderInvalidSerializer(ModelSerializer):
    reason = CharField(source='verbose_reason_type')
    shop = BriefShopSerializer(many=False)

    class Meta:
        model = OrderInvalid
        fields = ("id", "reason", "shop", "order_id", "reason_description", "json", "create_time", "update_time")