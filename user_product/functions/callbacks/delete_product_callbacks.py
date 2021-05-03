from notification.enums.message_types import MessageType
from notification.services import send_notification_task
from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobCallbackService, WebhookJobRecoveryService
from user_product.constants.shop_user_product_sync_status import ShopUserProductSyncStatus
from .create_product_callbacks import build_sync_product_from_shop_user_product_id_function

# ------------------------------------
from user_product.functions.delete_product.check_user_product_delete import check_user_product_delete
from user_product.functions.delete_product.delete_product_in_shop import delete_product_in_shop

delete_product_request_type = RequestType.ADAPTER_DELETE_PRODUCT


def delete_product_in_shop_successful_callback(shop_user_product, response):
    shop_user_product.sync_status = ShopUserProductSyncStatus.DELETED
    shop_user_product.sync_status_message = "Deleted successfully"
    shop_user_product.save()


def delete_product_in_shop_failed_callback(shop_user_product, response):
    shop_user_product.sync_status = ShopUserProductSyncStatus.ERROR
    shop_user_product.save()
    user_product = shop_user_product.user_product
    params = {
        "product_id": user_product.id,
        "product_name": user_product.title,
        "shop_list": shop_user_product.shop.url
    }
    send_notification_task.delay(user_product.user_id, MessageType.USER_PRODUCT_DELETE, params)


delete_product_in_shop_from_shop_user_product_id = build_sync_product_from_shop_user_product_id_function(
    delete_product_in_shop)

WebhookJobCallbackService.register_callbacks(request_type=delete_product_request_type,
                                             callbacks=(delete_product_in_shop_successful_callback,
                                                        delete_product_in_shop_failed_callback))

WebhookJobRecoveryService.register_function(request_type=delete_product_request_type,
                                            function=delete_product_in_shop_from_shop_user_product_id)
