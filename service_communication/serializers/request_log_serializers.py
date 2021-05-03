import json

from generic_relations.relations import GenericRelatedField
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from HUB import logger
from billing.models import Invoice
from billing.serializers import GenericRelationInvoiceSerializer
from order.models import Order
from order.serializers import GenericRelationOrderSerializer
from service_communication.models import ServiceCommunicationLog
from service_communication.serializers import WebhookJobSerializer
from shop.models import Shop
from shop.serializers.shop import GenericRelationShopSerializer
from user_product.models import UserProduct, ShopUserProduct, UserProductArtworkFusion
from user_product.serializers import GenericRelationShopUserProductSerializer, GenericRelationUserProductSerializer, \
    GenericRelationUserProductArtworkSerializer


class BriefRequestLogSerializer(ModelSerializer):
    relate_object = GenericRelatedField({
        Order: GenericRelationOrderSerializer(),
        ShopUserProduct: GenericRelationShopUserProductSerializer(),
        UserProduct: GenericRelationUserProductSerializer(),
        UserProductArtworkFusion: GenericRelationUserProductArtworkSerializer(),
        Shop: GenericRelationShopSerializer(),
        Invoice: GenericRelationInvoiceSerializer(),
    })
    webhook_job = WebhookJobSerializer()

    class Meta:
        model = ServiceCommunicationLog
        fields = ['id', 'relate_object', 'type', 'webhook_job', 'status_code',
                  'response_body', 'request_time', 'response_time', 'payload']


class BriefRequestLogWithProcessCode(BriefRequestLogSerializer):
    process_code = SerializerMethodField()

    @staticmethod
    def get_process_code(instance):
        try:
            response_body = json.loads(instance.response_body)
            process_code = []
            if 'purchase_units' in response_body:
                for purchase_unit in response_body.get('purchase_units'):
                    if 'payments' in purchase_unit and 'captures' in purchase_unit.get('payments'):
                        for capture in purchase_unit.get('payments').get('captures'):
                            if 'processor_response' in capture and 'response_code' in capture.get('processor_response'):
                                process_code.append(capture.get('processor_response').get('response_code'))
            return ', '.join(process_code)
        except Exception as e:
            logger.info(e)
            return ''

    class Meta(BriefRequestLogSerializer.Meta):
        fields = BriefRequestLogSerializer.Meta.fields + ['process_code', ]

# class WebhookJobSerializer(BriefWebhookJobSerializer):
#     class Meta(BriefWebhookJobSerializer.Meta):
#         pass
