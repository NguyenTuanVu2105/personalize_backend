import logging
import traceback

from django.core.exceptions import ValidationError
from django.db import transaction

from HUB.exceptions.FormValidationError import FormValidationError
from helper.datetime_helpers import get_current_datetime
from order.constants.invalid_reason_types import InvalidReasonType
from order.constants.order_types import OrderTypes
from order.forms import SampleOrderForm, CustomerInfoForm
from order.forms.order_shipping_address import OrderShippingAddressForm
from order.functions import save_order_item
from order.functions.traceback_order_invalid import traceback_order_invalid
from order.services.order_cost_service import update_order_cost
from order.services.service_order import OrderItemInvalidException, split_order_packs, OrderExistedException, \
    append_order_branding_card
from order.services.user_order import update_fulfillment_settings
from shop.models import Shop, Ecommerce

logger = logging.getLogger(__name__)


def create_sample_order(request_data, user):
    try:
        order_obj = initialize_new_sample_order(request_data, user)
    except OrderExistedException:
        traceback_order_invalid(request_data, InvalidReasonType.ORDER_EXISTED)
        raise FormValidationError(field="order", code="existed")
    except OrderItemInvalidException:
        traceback_order_invalid(request_data, InvalidReasonType.ITEM_NOT_IN_PRINTHOLO)
        raise ValidationError(code="order_item", message={"user_variant": "Invalid order items"})
    except Exception as e:
        logger.info((str(e)))
        traceback.print_tb(e.__traceback__)
        traceback_order_invalid(request_data, InvalidReasonType.OTHER)
        raise Exception
    split_order_packs(order_obj)
    update_order_cost(order_obj, reload_order=True)
    return order_obj


@transaction.atomic()
def initialize_new_sample_order(request_data, user):
    printholo_ecommerce = Ecommerce.objects.filter(name__contains="PrintHolo").first()
    printholo_store = Shop.objects.filter(owner_id=user.id, ecommerce=printholo_ecommerce).first()

    customer_data = request_data.get("customer", {})
    customer_info_pk = save_customer(customer_data=customer_data)

    shipping_address_form = OrderShippingAddressForm(data=request_data.get("shipping_address"))
    shipping_address_form.validate()
    shipping_address = shipping_address_form.save()

    items = request_data.get("items")
    order_obj = save_order(request_data, customer_info_pk, shipping_address, items, printholo_store)
    item_count = save_order_item(items, user, order_obj)

    if item_count <= 0:
        raise OrderItemInvalidException
    elif item_count < len(items):
        traceback_order_invalid(request_data, InvalidReasonType.ITEM_NOT_IN_PRINTHOLO)

    append_order_branding_card(order_obj)
    update_fulfillment_settings(order_obj)

    return order_obj


def save_customer(customer_data):
    if customer_data.get("customer_id"):
        customer_info_form = CustomerInfoForm(data=customer_data)
        customer_info_form.validate()
        customer_info_obj = customer_info_form.save()
        return customer_info_obj.pk
    else:
        return None


def save_order(request_data, customer_info_pk, shipping_address, items, printholo_store):
    order_form = SampleOrderForm(
        data={**request_data,
              "customer_info": customer_info_pk,
              "shipping_address": shipping_address.pk,
              "country_code": shipping_address.country_code,
              "total_items": len(items),
              "type": OrderTypes.PRINTHOLO,
              "shop": printholo_store.pk if printholo_store else None,
              "order_id": None,
              "order_number": None,
              "seller_edit_time": get_current_datetime()
              })
    order_form.validate()
    order_obj = order_form.save()
    return order_obj
