from order.constants.invalid_reason_types import InvalidReasonType, DescriptionInvalidReason
from order.models import Order
from order.models.order_invallid import OrderInvalid
from shop.constants.shop_status import ShopStatus
from shop.models import Shop
from user_product.constants import UserProductStatus
from user_product.models import UserVariant


def traceback_order_invalid(order_obj, error_type, description=None):
    if error_type != InvalidReasonType.SHOP_INVALID:
        shop = Shop.objects.filter(url=order_obj.get("shop_url"), status=ShopStatus.ACTIVE).first()
    else:
        shop = None
    OrderInvalid.objects.update_or_create(order_id=str(order_obj['order_id']),
                                          defaults={
                                              "shop": shop,
                                              "reason_code": error_type,
                                              "reason_description": description or DescriptionInvalidReason[error_type],
                                              "json": order_obj
                                          }
                                          )


def is_valid_exist_order(request_data):
    order_id = request_data['order_id']
    if Order.objects.filter(order_id=order_id).exists():
        traceback_order_invalid(request_data, InvalidReasonType.ORDER_EXISTED)
        return False
    return True


def is_valid_shop(request_data):
    shop = Shop.objects.filter(url=request_data.get("shop_url"), status=ShopStatus.ACTIVE).first()
    if not shop:
        traceback_order_invalid(request_data, InvalidReasonType.SHOP_INVALID)
        return False
    return True


def is_valid_items(request_data):
    items = request_data.get("items")
    shop = Shop.objects.filter(url=request_data.get("shop_url"), status=ShopStatus.ACTIVE).first()
    for item in items:
        sku = item.get("sku")
        if sku:
            user_variant = UserVariant.objects.filter(sku=sku,
                                                      user_product__status=UserProductStatus.ACTIVE,
                                                      user_product__shop=shop,
                                                      user_product__user=shop.owner
                                                      ).first()
            if user_variant:
                return True
    traceback_order_invalid(request_data, InvalidReasonType.ITEM_NOT_IN_PRINTHOLO)
    return False


def is_valid_paid(request_data):
    paid = request_data.get('financial_status') == 'paid'
    if not paid:
        traceback_order_invalid(request_data, InvalidReasonType.UNPAID_ORDER)
        return False
    return True
