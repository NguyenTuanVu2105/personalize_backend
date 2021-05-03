from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from rest_framework.fields import FloatField
from rest_framework.serializers import ModelSerializer, CharField

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from billing.constants.transaction_statuses import TransactionStatus
from billing.models import Refund, Transaction, Invoice
from coupon.serializers.user import UserBriefCouponSerializer
from order.models import Order
from order.serializers.order_shipping_address import OrderShippingAddressSerializer, \
    FulfillServiceShippingAddressSerializer
from service_communication.constants.request_type import RequestType
from shop.models import Shop
from shop.serializers.shop import BriefShopSerializer
from system_metadata.serializers.shipping_rate import ShippingRateSerializer
from user.contants.tracking_generation_time import get_track_generation_json
from user.models import UserSettings
from user.serializers.user import BriefUserSerializer, BriefUserWithPaymentSerializer
from .customer_info import CustomerInfoSerializer
from .order_comments import OrderCommentsSerializer
from .order_history import OrderHistorySerializer
from .order_item import FulfillServiceOrderItemSerializer
from .order_pack import OrderPackSerializer, OrderPackWithInvoicesSerializer


class GenericRelationOrderSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = Order


class BriefOrderSerializer(GenericRelationOrderSerializer):
    customer_info = CustomerInfoSerializer(many=False)
    shop = BriefShopSerializer(many=False)
    fulfill_status = CharField(source="verbose_fulfill_status")
    financial_status = CharField(source="verbose_financial_status")
    total_base_cost = FloatField(source="production_cost")
    total_shipping_cost = FloatField(source="shipping_cost")

    class Meta(GenericRelationOrderSerializer.Meta):
        fields = (
            "id", "order_id", "order_number", "is_item_editable", "is_coupon_editable",
            "is_shipping_address_editable",
            "is_shipping_rate_editable", "is_cancellable", "shop", "tags", "note", "financial_status", "fulfill_status",
            "customer_info", "total_shipping_cost", "total_base_cost", "total_cost", "cached_metadata", "create_time",
            "update_time", "unresolved_support_ticket_count", "support_ticket_count")


class BriefAdminOrderSerializer(BriefOrderSerializer):
    user = BriefUserSerializer(source="shop.owner")
    shipping_address = OrderShippingAddressSerializer()

    class Meta(BriefOrderSerializer.Meta):
        fields = (
            "id", "order_id", "order_number", "shop", "tags", "note", "financial_status", "fulfill_status",
            "customer_info", "total_shipping_cost", "total_base_cost", "total_cost", "total_mfr_cost",
            "create_time", "update_time", "user", 'shipping_address', "is_delivered_order", "is_send_mail_add_payment")


class BriefAdminOrderWithInvoicesSerializer(BriefAdminOrderSerializer):
    packs = OrderPackWithInvoicesSerializer(many=True)

    class Meta(BriefAdminOrderSerializer.Meta):
        fields = BriefAdminOrderSerializer.Meta.fields + ('packs',)


class OrderSerializer(BriefOrderSerializer):
    packs = OrderPackSerializer(many=True)
    shipping_address = OrderShippingAddressSerializer()
    shipping_rate = ShippingRateSerializer()
    histories = OrderHistorySerializer(source="order_histories", many=True)
    applied_coupons = UserBriefCouponSerializer(many=True)
    refund_amount = serializers.SerializerMethodField()

    def get_refund_amount(self, instance):
        try:
            order_content_type = ContentType.objects.filter(model='order').first()
            refunds = Refund.objects.filter(object_id=instance.id, content_type=order_content_type)
            refund_content_type = ContentType.objects.filter(model="refund").first()
            transactions = Transaction.objects.filter(content_type=refund_content_type,
                                                      status=TransactionStatus.SUCCESS)
            refund_real_amount = 0
            for refund in refunds:
                transaction = transactions.filter(object_id=refund.id).first()
                if transaction:
                    if "amount" in transaction.detail:
                        refund_real_amount += float(transaction.detail["amount"]['total'])
            return refund_real_amount
        except ValueError as e:
            return 0

    class Meta(BriefOrderSerializer.Meta):
        fields = (
            "id", "order_id", "order_number", "is_item_editable", "is_coupon_editable", "is_shipping_address_editable",
            "is_shipping_rate_editable", "is_cancellable", "shop", "tags", "note", "financial_status", 'refund_amount',
            "fulfill_status", "production_cost", "shipping_cost", "discount", "total_cost", "total_price", "packs",
            "customer_info", "shipping_address", "create_time", "update_time", "shipping_rate", "histories",
            "unresolved_support_ticket_count", "support_ticket_count", "cached_metadata", "applied_coupons",
            "can_request_fulfillment", "is_shipping_city_editable", "is_item_addable", "seller_edit_time",
            "edit_order_items_delay", "request_order_processing_manually")


class AdminOrderSerializer(OrderSerializer):
    user = BriefUserWithPaymentSerializer(source="shop.owner")
    histories = OrderHistorySerializer(source="order_histories", many=True)
    comments = OrderCommentsSerializer(source="order_comments", many=True)
    request_logs = serializers.SerializerMethodField()

    @staticmethod
    def get_request_logs(instance):
        from service_communication.models import ServiceCommunicationLog
        from service_communication.serializers import BriefRequestLogWithProcessCode
        related_invoice_ids = Invoice.objects.filter(packs__order_pack__order_id=instance.id) \
            .values_list('id', flat=True).order_by()
        order_content_type = ContentType.objects.get_for_model(instance).id
        invoice_content_type = ContentType.objects.get(app_label='billing', model='invoice').id
        request_logs = ServiceCommunicationLog.objects \
            .filter(Q(type=RequestType.PAYMENT_PAYONEER_CHARGE) | Q(type=RequestType.PAYMENT_PAYPAL_REQUEST)) \
            .filter((Q(content_type=order_content_type) & Q(object_id=instance.id)) |
                    (Q(content_type=invoice_content_type) & Q(object_id__in=related_invoice_ids))). \
            order_by('-request_time')
        return BriefRequestLogWithProcessCode(request_logs, many=True).data

    class Meta(OrderSerializer.Meta):
        fields = (
            "id", "order_id", "order_number", "shop", "tags", "note", "financial_status", "fulfill_status", "packs",
            "customer_info", "shipping_address", "create_time", "update_time", "user", 'histories', "production_cost",
            "shipping_cost", "discount", "total_cost", "total_mfr_cost", "total_price_in_usd", "comments",
            'request_logs')


class FulfillServiceOrderSerializer(ModelSerializer):
    shipping_address = FulfillServiceShippingAddressSerializer()
    items = FulfillServiceOrderItemSerializer(many=True, source="get_fulfillable_item")
    namespace = serializers.CharField(source='shop.name')
    shipping_plan = serializers.CharField(source='shipping_rate.slug')

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        shipping_address = representation.pop('shipping_address')
        representation['address'] = shipping_address
        shop_id = representation.pop('shop')
        shop = Shop.objects.get(id=shop_id)
        user_setting = UserSettings.objects.get(user_id=shop.owner_id)
        preference = get_track_generation_json(user_setting.tracking_generation_time)
        representation['preference'] = preference
        representation['order_paid_at'] = representation['update_time']
        return representation

    class Meta:
        model = Order
        fields = (
            "id", "order_id", "namespace", "tags", "note", "financial_status", "items",
            "shipping_address", "create_time", "update_time", "shipping_plan", "shop")
