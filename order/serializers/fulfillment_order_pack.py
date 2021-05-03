from rest_framework.serializers import ModelSerializer, CharField

from order.models import FulfillmentOrderPack


class FulfillmentOrderPackSerializer(ModelSerializer):
    tracking_status = CharField(source="verbose_tracking_status")

    class Meta:
        model = FulfillmentOrderPack
        fields = ("tracking_status", "tracking_company", "tracking_number", "tracking_url",
                  "origin_tracking_url", "update_time")


class MerchantServiceFulfillmentOrderPackTrackingSerializer(FulfillmentOrderPackSerializer):
    class Meta(FulfillmentOrderPackSerializer.Meta):
        fields = ('id', "tracking_id", "tracking_status", "tracking_company", "tracking_number", "tracking_url",
                  "origin_tracking_url", "update_time")


class UpdatableFulfillmentPackSerializer(ModelSerializer):
    tracking_status_verbose = CharField(source="verbose_tracking_status")

    class Meta:
        model = FulfillmentOrderPack
        fields = (
            'id', "tracking_id", "tracking_status", "tracking_company", "tracking_number", 'tracking_status_verbose',
            "tracking_url", "origin_tracking_url", "update_time", 'manually_update')
