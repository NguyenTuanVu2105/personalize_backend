from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from order.models import CancelShippingRequest


class BriefCancelShippingRequestSerializer(ModelSerializer):
    status = CharField(source="verbose_status")

    class Meta:
        model = CancelShippingRequest
        fields = (
            "id", "note", "admin_note", "status", "approve_time", "create_time", "update_time")


class OrderCancelShippingRequestDetailSerializer(BriefCancelShippingRequestSerializer):
    order_packs = SerializerMethodField()

    def get_order_packs(self, obj):
        from order.serializers.order_pack import OrderPackSerializer
        return OrderPackSerializer(obj.order_packs, many=True).data

    class Meta(BriefCancelShippingRequestSerializer.Meta):
        fields = (
            "id", "note", "admin_note", "status", "approve_time", "create_time", "update_time", "order", "order_packs",
            "admin", "user")
