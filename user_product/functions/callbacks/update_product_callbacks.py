from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobCallbackService, WebhookJobRecoveryService
from user_product.constants.shop_user_product_sync_status import ShopUserProductSyncStatus
from user_product.functions.sync_product_in_shop.update_product import update_product_in_shop
from .create_product_callbacks import build_sync_product_from_shop_user_product_id_function

# ------------------------------------
update_product_request_type = RequestType.ADAPTER_UPDATE_PRODUCT


def update_product_in_shop_successful_callback(shop_user_product, response):
    shop_user_product.sync_status = ShopUserProductSyncStatus.SYNCED
    shop_user_product.handle = response['product']['handle']
    shop_user_product.sync_status_message = "Synced successfully"
    shop_user_product.save()


def update_product_in_shop_failed_callback(shop_user_product, response):
    shop_user_product.sync_status = ShopUserProductSyncStatus.ERROR
    shop_user_product.save()


update_product_in_shop_from_shop_user_product_id = build_sync_product_from_shop_user_product_id_function(
    update_product_in_shop)

WebhookJobCallbackService.register_callbacks(request_type=update_product_request_type,
                                             callbacks=(update_product_in_shop_successful_callback,
                                                        update_product_in_shop_failed_callback))

WebhookJobRecoveryService.register_function(request_type=update_product_request_type,
                                            function=update_product_in_shop_from_shop_user_product_id)
