from generic_relations.relations import GenericRelatedField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from order.models import Order
from order.serializers import GenericRelationOrderSerializer
from service_communication.models import WebhookJob
from shop.models import Shop
from shop.serializers.shop import GenericRelationShopSerializer
from user_product.models import UserProduct, ShopUserProduct, UserProductArtworkFusion
from user_product.serializers import GenericRelationShopUserProductSerializer, GenericRelationUserProductSerializer, \
    GenericRelationUserProductArtworkSerializer


class BriefWebhookJobSerializer(ModelSerializer):
    relate_object = GenericRelatedField({
        Order: GenericRelationOrderSerializer(),
        ShopUserProduct: GenericRelationShopUserProductSerializer(),
        UserProduct: GenericRelationUserProductSerializer(),
        UserProductArtworkFusion: GenericRelationUserProductArtworkSerializer(),
        Shop: GenericRelationShopSerializer(),
    })
    request_type = CharField(source="verbose_request_type")

    class Meta:
        model = WebhookJob
        fields = ['id', 'relate_object', 'request_type', 'status', 'attempted_count', 'max_attempt_count',
                  'is_recoverable', 'is_cancellable', 'update_time', 'payload']


class WebhookJobSerializer(BriefWebhookJobSerializer):
    class Meta(BriefWebhookJobSerializer.Meta):
        pass
