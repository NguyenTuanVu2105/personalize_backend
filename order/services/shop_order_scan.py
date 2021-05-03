import logging

from django.db.models import F
from django.utils import timezone

from order.services.service_order import create_order
from service_communication.services.adapter_services import AdapterOrderCommunicationService
from shop.constants.shop_status import ShopStatus
from shop.models import Shop, OrderScanInfo

logger = logging.getLogger(__name__)

ERROR_BUCKET_SIZE = 20
ERROR_DROP_RATE = 1
MAX_API_ERROR_COUNT = 5

ORDER_LIMIT_PER_CALL = 250
MAX_CACHED_ORDER_IDS = 1000


def check_all_shop_order():
    shops = Shop.objects.ecommerce_exclude().order_by(F('order_scan_info__update_time').asc(nulls_first=True)).filter(
        status=ShopStatus.ACTIVE, api_error_count__lt=MAX_API_ERROR_COUNT)[:5]
    for shop in shops:
        if not hasattr(shop, 'order_scan_info'):
            shop.order_scan_info = OrderScanInfo.objects.create(shop=shop)
        order_scan_info = shop.order_scan_info
        check_shop_order(order_scan_info)


def check_shop_order(order_scan_info):
    checked_order_ids = order_scan_info.checked_order_ids
    order_ids = []
    last_update = timezone.now()
    shop = order_scan_info.shop
    logger.info("Scanning orders of shop " + shop.url)
    try:
        response = AdapterOrderCommunicationService.get_order_by_update_time(shop)
        if response['success'] is not True:
            if 'error' in response:
                message = response['error']
            elif 'message' in response:
                message = response['message']['errors']
            else:
                message = str(response)
            raise RuntimeError(message)
        updated_orders = response["orders"]
        if len(updated_orders) >= ORDER_LIMIT_PER_CALL - 1:
            last_update = updated_orders(len(updated_orders) - 1).updated_time
        order_ids = list(map(lambda _order: _order["id"],
                             filter(lambda _order: _order["id"] not in checked_order_ids, updated_orders)))
        if len(order_ids) > 0:
            orders = AdapterOrderCommunicationService.get_list_order_by_id(shop, order_ids)['orders']
            for order_data in orders:
                try:
                    create_order(order_data)
                except Exception as e:
                    logger.exception(e)
                else:
                    logger.info(f'order {order_data["order_id"]} created')
    except Exception as e:
        logger.exception(e)
        last_update = order_scan_info.last_order_update_time
        shop.api_error_count += 1
        shop.save()
    checked_order_ids = checked_order_ids + order_ids
    checked_order_ids.sort()
    order_scan_info.last_order_update_time = last_update
    order_scan_info.checked_order_ids = checked_order_ids[max(len(checked_order_ids) - MAX_CACHED_ORDER_IDS, 0):]
    order_scan_info.save()
