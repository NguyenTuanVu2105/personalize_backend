from django.db.models.signals import pre_save
from django.dispatch import receiver

from notification.enums.message_types import MessageType
from order.models.shipping_address import OrderShippingAddress
from order.services.order_history import create_order_history_for_shipping_address_change
from order.services.service_order import sync_order_shipping_address, sync_adapter_order
from notification.services.notification import send_notification_task


@receiver([pre_save, ], sender=OrderShippingAddress)
def update_shipping_address(sender, instance, *args, **kwargs):
    if instance.id:
        new_shipping_address_obj = instance
        try:
            order = new_shipping_address_obj.order
            order.shipping_address = new_shipping_address_obj
        except AttributeError:
            return
        is_changed, is_country_code_changed, old_shipping_address_obj = new_shipping_address_obj.check_if_data_has_changed()
        if is_changed:
            is_approved = True
            if is_country_code_changed and not order.is_shipping_city_editable:
                is_approved = False
                send_notification_task.delay(order.shop.owner_id, MessageType.ORDER_SHIPPING_ADDRESS_UPDATE_REJECTED,
                                             {'order_id': order.id})
                instance.mark_as_not_save()
            else:
                if order.is_pushed_to_fulfillment:
                    sync_order_shipping_address(order)
                    sync_adapter_order(order)
            create_order_history_for_shipping_address_change(order, old_shipping_address_obj, new_shipping_address_obj,
                                                             is_approved)
