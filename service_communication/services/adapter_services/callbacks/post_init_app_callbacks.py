from service_communication.constants.request_type import RequestType
from service_communication.services.adapter_services import AdapterAppCommunicationService
from service_communication.services.webhook_job_services import WebhookJobCallbackService, WebhookJobRecoveryService
from shop.models import Shop

post_init_app_request_type = RequestType.ADAPTER_POST_INIT_APP

import logging
logger = logging.getLogger(__name__)




def post_init_app_successful_callback(shop, response):
    logger.info(response)
    location_id = response['data']['fulfillment']['location_id']
    shop.location_id = location_id
    shop.save()


def post_init_app_failed_callback(shop, response):
    pass


def build_post_init_app_from_shop_id_function(function):
    def get_objs_and_pass_to_function(shop_id):
        shop_obj = Shop.objects.filter(id=shop_id).first()
        if shop_obj:
            function(shop_obj)

    return get_objs_and_pass_to_function


post_init_app_from_shop_id = build_post_init_app_from_shop_id_function(AdapterAppCommunicationService.post_init_app)
WebhookJobCallbackService.register_callbacks(request_type=post_init_app_request_type,
                                             callbacks=(
                                                 post_init_app_successful_callback,
                                                 post_init_app_failed_callback))

WebhookJobRecoveryService.register_function(request_type=post_init_app_request_type,
                                            function=(post_init_app_from_shop_id))
