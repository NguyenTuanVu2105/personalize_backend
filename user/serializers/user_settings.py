from rest_framework import serializers

from ..models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    is_charge_halted = serializers.BooleanField(source="is_invoices_charge_unlockable")
    default_branding_card_product = serializers.SerializerMethodField()

    @staticmethod
    def get_default_branding_card_product(instance):
        return instance.default_branding_card.user_product.id if instance.default_branding_card is not None else None

    class Meta:
        model = UserSettings
        fields = (
            'id', 'user', 'is_charge_halted', "timezone", "edit_order_items_delay", "last_create_support_ticket_time",
            "tracking_generation_time", "request_order_processing_manually", 'default_branding_card',
            'default_branding_card_product')
