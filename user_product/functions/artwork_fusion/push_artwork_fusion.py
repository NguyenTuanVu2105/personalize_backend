import logging

from order.constants.order_types import OrderTypes
from order.models import OrderItem
from service_communication.constants.request_type import RequestType
from service_communication.models import WebhookJob
from service_communication.services.cancel_webhook_job import bulk_cancel_webhook_job
from shop.models import Shop, Ecommerce
from user_product.models import ShopUserProduct
from ..update_fulfill_artwork import sync_artwork_by_shop

logger = logging.getLogger(__name__)


def push_artwork_fusion(user_product_artwork_fusion, artwork_fusion=None):
    user_product = user_product_artwork_fusion.user_product
    jobs = WebhookJob.objects.filter(request_type=RequestType.FULFILL_PUSH_ARTWORK,
                                     object_id=user_product_artwork_fusion.id)

    if jobs.processing():
        return False, "Pushing old version is in progress. Please wait and try again!"

    else:
        jobs = jobs.cancelable_filter().values_list("id", flat=True)
        success = bulk_cancel_webhook_job(jobs)
        if success:
            if artwork_fusion:
                artwork_fusion.save()

            order_items = OrderItem.objects.filter(user_variant__user_product=user_product)
            shops = [order_item.order.shop for order_item in order_items]
            for shop in set(shops):
                shop_user_product = ShopUserProduct.objects.filter(user_product=user_product,
                                                                   shop=shop).first()
                if shop_user_product:
                    sync_artwork_by_shop(user_product_artwork_fusion, shop)

            printholo_ecommerce = Ecommerce.objects.filter(name__contains="PrintHolo").first()
            for order_item in order_items:
                order = order_item.order
                if order.type == OrderTypes.PRINTHOLO:
                    user_shop = Shop.objects.filter(owner=user_product.user,
                                                    ecommerce=printholo_ecommerce).first()
                    sync_artwork_by_shop(user_product_artwork_fusion, user_shop)
                    break

            return True, "Pushing fusion artwork is in progress!"

        else:
            return False, "Pushing an old version is in progress. Please wait and try again!"
