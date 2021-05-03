from user_product.functions.sync_product_in_shop.create_product import create_product_in_shop
from user_product.models import ShopUserProduct
from service_communication.services.webhook_job_services import WebhookJobCallbackService, WebhookJobRecoveryService
from service_communication.constants.request_type import RequestType
from user_product.constants.shop_user_product_sync_status import ShopUserProductSyncStatus

# ------------------------------------
create_product_request_type = RequestType.ADAPTER_ADD_NEW_PRODUCT


def build_sync_product_from_shop_user_product_id_function(function):
    def get_objs_and_pass_to_function(shop_user_product_id):
        shop_user_product_obj = ShopUserProduct.objects.filter(id=shop_user_product_id).first()
        if shop_user_product_obj:
            function(shop_user_product_obj)

    return get_objs_and_pass_to_function


def create_product_in_shop_successful_callback(shop_user_product, response):
    shop_user_product.sync_status = ShopUserProductSyncStatus.SYNCED
    shop_user_product.product_id = response['product']['id']
    shop_user_product.handle = response['product']['handle']
    shop_user_product.sync_status_message = "Synced successfully"
    shop_user_product.save()


def create_product_in_shop_failed_callback(shop_user_product, response):
    shop_user_product.sync_status = ShopUserProductSyncStatus.ERROR
    shop_user_product.save()


create_product_in_shop_from_shop_user_product_id = build_sync_product_from_shop_user_product_id_function(
    create_product_in_shop)

WebhookJobCallbackService.register_callbacks(request_type=create_product_request_type,
                                             callbacks=(create_product_in_shop_successful_callback,
                                                        create_product_in_shop_failed_callback))

WebhookJobRecoveryService.register_function(request_type=create_product_request_type,
                                            function=create_product_in_shop_from_shop_user_product_id)
