# ------------------------------------
from django.db.models.functions import Now

from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobRecoveryService, WebhookJobCallbackService
from user_product.functions.artwork_fusion import generate_artwork_fusion
from user_product.functions.artwork_fusion.update_user_product_generate_fusion import \
    update_user_product_generate_fusion
from user_product.models import UserProductArtworkFusion


def generate_artwork_fusion_successful_callback(user_product_artwork_fusion, response):
    user_product = user_product_artwork_fusion.user_product
    artwork_fusion = user_product_artwork_fusion.artwork_fusion
    artwork_fusion.original_image_path = response["storage_path"]
    artwork_fusion.image_url = response["storage_url"]
    artwork_fusion.last_fusion_update_time = Now()
    artwork_fusion.save()

    if user_product.additional_fusion_sides:
        from user_product.functions.artwork_fusion import copy_user_product_artwork_fusion
        copy_user_product_artwork_fusion(user_product_artwork_fusion)

    user_product_artwork_fusion = artwork_fusion.user_product_artwork_fusion_set.first()
    if user_product_artwork_fusion:
        user_product = user_product_artwork_fusion.user_product
        update_user_product_generate_fusion(user_product)


def generate_artwork_fusion_failed_callback(user_product_artwork_fusion, response):
    pass


def build_generate_artwork_fusion_from_fusion_id_function(function):
    def get_objs_and_pass_to_function(fusion_id):
        fusion_obj = UserProductArtworkFusion.objects.filter(id=fusion_id).first()
        if fusion_obj:
            function(fusion_obj)

    return get_objs_and_pass_to_function


generate_artwork_fusion_request_type = RequestType.MOCKUP_GENERATE_ARTWORK_FUSION
generate_artwork_fusion_from_fusion_id = build_generate_artwork_fusion_from_fusion_id_function(generate_artwork_fusion)

WebhookJobRecoveryService.register_function(request_type=generate_artwork_fusion_request_type,
                                            function=generate_artwork_fusion_from_fusion_id)

WebhookJobCallbackService.register_callbacks(request_type=generate_artwork_fusion_request_type,
                                             callbacks=(generate_artwork_fusion_successful_callback,
                                                        generate_artwork_fusion_failed_callback))
