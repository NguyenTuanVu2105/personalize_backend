from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobRecoveryService
from shop.models import Shop
from user_product.functions.update_fulfill_artwork import sync_artwork_by_shop
from user_product.models import UserProductArtworkFusion

# ------------------------------------
sync_artwork_request_type = RequestType.FULFILL_PUSH_ARTWORK


def build_sync_artwork_by_shop_from_user_product_artwork_id_and_shop_id_function(function):
    def get_objs_and_pass_to_function(user_product_artwork_id, shop_id):
        user_product_artwork_obj = UserProductArtworkFusion.objects.filter(id=user_product_artwork_id).first()
        shop_obj = Shop.objects.filter(id=shop_id).first()
        if shop_obj and user_product_artwork_obj:
            function(user_product_artwork_obj, shop_obj)

    return get_objs_and_pass_to_function


sync_artwork_from_user_product_artwork_id_and_shop_id = build_sync_artwork_by_shop_from_user_product_artwork_id_and_shop_id_function(
    sync_artwork_by_shop)

WebhookJobRecoveryService.register_function(request_type=sync_artwork_request_type,
                                            function=sync_artwork_from_user_product_artwork_id_and_shop_id)
