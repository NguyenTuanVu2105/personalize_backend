import logging
from datetime import timedelta

from django.db.models import Prefetch, Q
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.list_model_mixins import ListWithUserSettingsModelMixin
from HUB.viewsets.mixins.retrieve_model_mixins import RetrieveWithUserSettingsModelMixin
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from coupon.services.coupon_transaction.coupon_redeeming import cancel_all_applied_coupon_in_order
from helper.datetime_helpers import get_current_datetime
from notification.enums.message_types import MessageType
from notification.services import send_notification_task
from order.constants.fulfill_statuses import OrderFulfillStatus, OrderPackFulfillStatus
from order.constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus
from order.filters import OrderFilter
from order.functions.send_order_add_payment_mail import send_order_add_payment_mail
from order.functions.send_order_review_mail import send_order_review_mail
from order.models import Order, OrderItem, OrderPack, FulfillmentOrderPack
from order.paginations import OrderPagination
from order.serializers import OrderSerializer, BriefOrderSerializer
from order.serializers.order_cost_serializer import SampleOrderPackSerializer
from order.services import create_cancel_shipping_request, create_sample_order
from order.services.order_cost_service import update_order_cost
from order.services.order_history import create_order_history_for_order_item_remove
from order.services.order_pack_tracking import sync_cancelled_fulfillment_packs
from order.services.order_pack_tracking_scan import check_all_unknown_tracking, check_all_order_pack_tracking
from order.services.order_status import update_order_static_fulfill_status, update_order_static_financial_status, \
    get_order_fulfill_status
from order.services.service_order import prepare_to_charge_order, calculate_fake_order
from order.services.user_order import update_order
from order.tasks.scan_and_send_mail_add_payment import scan_and_send_mail_add_payment
from order.tasks.scan_and_send_mail_review_order import scan_and_send_mail_review_orders
from shipping.models import ShippingCountry, ShippingRate
from user_product.models import UserVariant

logger = logging.getLogger(__name__)


class UserOrderViewSet(SearchableListModelMixin,
                       RetrieveWithUserSettingsModelMixin,
                       ListWithUserSettingsModelMixin,
                       mixins.CreateModelMixin,
                       AuthenticatedGenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filterset_class = OrderFilter
    ordering_fields = ['order_number', 'create_time', 'update_time', 'customer_info__last_name',
                       'customer_info__first_name', 'total_cost']

    error_messages = {
        "order_item": {
            "not_allow_edit": "Item is not allowed to edit",
            "not_found": "Cannot found order item"
        },
        "calculate_cost": {
            "invalid_user_variant": "Some user variant is invalid"
        }
    }

    def get_queryset(self):
        return self.queryset. \
            filter_by_user_id(self.request.user.pk). \
            select_related('shop', 'shop__currency', 'shop__ecommerce', 'customer_info',
                           'shipping_address')

    def get_brief_queryset(self):
        return self.queryset.filter_by_user_id(self.request.user.pk)

    def list(self, request, *args, **kwargs):
        self.serializer_class = BriefOrderSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        order_obj = create_sample_order(request_data=request.data, user=request.user)
        return Response({"success": True, "order_id": order_obj.pk})

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        updated_order_obj = update_order(order, request.data, request.user)
        updated_order_obj = Order.objects.include_pack_fulfill_statuses().filter(pk=updated_order_obj.pk).first()
        fulfill_status = get_order_fulfill_status(updated_order_obj)
        logger.info(fulfill_status)
        if updated_order_obj.fulfill_status == OrderFulfillStatus.UNFULFILLED:
            update_order_cost(updated_order_obj)
        return Response({"success": True})

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().prefetch_related('packs',
                                                             'packs__cancel_shipping_requests',
                                                             'packs__invoice_pack',
                                                             'packs__items',
                                                             'order_histories',
                                                             Prefetch("packs__items__user_variant",
                                                                      UserVariant.objects.prefetch_related_objects()))
        return super().retrieve(request, *args, **kwargs)

    MAX_NUMBER_OF_ORDER_ID = 500
    ALLOWED_TIME_SUPPORT_ORDER_OLDER_IN_DAYS = 30

    @action(methods=["GET"], detail=False, url_path="ids")
    def list_ids(self, request):
        date_limit = get_current_datetime() - timedelta(days=self.ALLOWED_TIME_SUPPORT_ORDER_OLDER_IN_DAYS)
        ids = self.get_brief_queryset().filter(update_time__gt=date_limit).values_list("id", flat=True)[
              :self.MAX_NUMBER_OF_ORDER_ID]
        return Response({"success": True, "order_ids": ids})

    @staticmethod
    def cancel_order_execute(order_obj, user_id):
        if not order_obj.is_cancellable:
            return Response({"success": False, "error": "NOT_ALLOWED"})
        cancelled_packs = order_obj.packs.bulk_set_canceled()
        sync_cancelled_fulfillment_packs(order_obj, cancelled_packs)
        update_order_static_fulfill_status(order_obj)
        update_order_static_financial_status(order_obj)
        cancel_all_applied_coupon_in_order(order_obj)
        send_notification_task.delay(user_id, MessageType.CANCEL_ORDER_SUCCESS,
                                     {'order_id': order_obj.id})
        # send_notification_task.delay(user_id, MessageType.CANCEL_ORDER_SUCCESS_SHOP_OWNER,
        #                              {'order_id': order_obj.order_id}, [order_obj.shop.email])
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="cancel_order")
    def cancel_order(self, request):
        order_obj = self.get_queryset().get(id=request.data['id'])
        return self.cancel_order_execute(order_obj=order_obj, user_id=self.request.user.pk)

    @action(methods=["POST"], detail=False, url_path="cancel_order_last_item")
    def remove_last_item_and_cancel_order(self, request):
        order_obj = self.get_queryset().get(id=request.data['order_id'])
        order_item_obj = order_obj.items.filter(id=request.data['item_id']).first()
        if not order_item_obj:
            raise FormValidationError(field="order_item", code="not_found")
        elif order_item_obj.order_pack.fulfill_status != OrderPackFulfillStatus.UNFULFILLED:
            raise FormValidationError(field="order_item", code="not_allow_edit")
        else:
            from order.services.order_cost_service import update_order_cost
            create_order_history_for_order_item_remove(order_obj=order_obj, order_item_obj=order_item_obj)
            order_pack = order_item_obj.order_pack
            order_item_obj.delete()
            order_pack.delete()

            cancel_all_applied_coupon_in_order(order_obj)
            update_order_cost(order_obj)

        return self.cancel_order_execute(order_obj=order_obj, user_id=self.request.user.pk)

    @action(methods=["POST"], detail=False, url_path="cancel_shipping")
    def cancel_shipping(self, request):
        request_data = request.data
        user = request.user
        order_obj = self.get_queryset().get(id=request_data.get("id"))
        order_pack_ids = request_data.get("packs", [])
        create_cancel_shipping_request(user, order_obj, order_pack_ids)
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="request_fulfill")
    def request_fulfill(self, request):
        order_id = request.data['id']
        try:
            order_obj = self.get_queryset().get(id=order_id, fulfill_status=OrderFulfillStatus.UNFULFILLED)
            prepare_to_charge_order(order_obj)
            return Response({"success": True})
        except Order.DoesNotExist:
            return Response({"success": False, "message": "Order status is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, url_path="cost")
    def calculate_order_cost(self, request, *args, **kwargs):
        # TODO USE FORM TO VALIDATE
        request_data = request.data

        shipping_data = request_data.get("shipping")
        items_data = request_data.get("items")

        user_variant_id_item_map = dict(map(lambda item: (item["user_variant"], item), items_data))
        user_variants = UserVariant.objects.select_related("abstract_variant").filter(
            user_product__user_id=self.request.user.pk, id__in=user_variant_id_item_map.keys())
        if len(user_variants) < len(items_data):
            raise FormValidationError(field="calculate_cost", code="invalid_user_variant")
        items = list(map(lambda variant: OrderItem(user_variant=variant,
                                                   quantity=user_variant_id_item_map.get(variant.id)["quantity"]),
                         user_variants))

        shipping_zone = ShippingCountry.objects.filter(code=shipping_data["country"]).first().zone
        shipping_rate = ShippingRate.objects.get(pk=shipping_data["rate"])

        packs, total_production_cost, total_shipping_cost = calculate_fake_order(items, shipping_zone, shipping_rate)

        return Response({"success": True,
                         "packs": SampleOrderPackSerializer(instance=packs, many=True).data,
                         "total_production_cost": total_production_cost,
                         "total_shipping_cost": total_shipping_cost,
                         "total_cost": total_production_cost + total_shipping_cost})

    @action(methods=["POST"], detail=False, url_path="test")
    def test(self, request, *args, **kwargs):
        check_all_order_pack_tracking()
        return Response("ok")
