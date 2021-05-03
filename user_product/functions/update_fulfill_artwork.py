import logging

from celery.decorators import task

from HUB.constants.celery_task import CeleryTask
from order.models import OrderItem
from service_communication.services.fulfill_services import FulfillProductCommunicationService
from user_product.models import Artwork, ShopUserProduct

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_UPDATE_FULFILL_ARTWORK)
def update_fulfill_artwork(artwork_id):
    try:
        artwork = Artwork.objects.get(id=artwork_id)
    except Artwork.DoesNotExist:
        raise Artwork.DoesNotExist()
    else:
        user_product_artworks = [user_product_artwork for user_product_artwork in
                                 artwork.user_product_artwork_set.all()]
        user_products = [user_product_artwork.user_product for user_product_artwork in user_product_artworks]
        shops = [order_item.order.shop for order_item in
                 OrderItem.objects.filter(user_variant__user_product__in=user_products)]
        for user_product_artwork in set(user_product_artworks):
            user_product = user_product_artwork.user_product
            for shop in set(shops):
                shop_user_product = ShopUserProduct.objects.filter(user_product=user_product, shop=shop).first()
                if shop_user_product:
                    sync_artwork_by_shop(user_product_artwork, shop)


def sync_artwork_by_shop(user_product_artwork, shop):
    user_product = user_product_artwork.user_product
    extra_artwork = user_product.abstract_product.meta.pricing_meta["extra_artwork"]
    artwork_fusion = user_product_artwork.artwork_fusion
    layer_count = artwork_fusion.artwork_fusion_info_artwork_set.count()
    if extra_artwork != 0 and layer_count == 0 and not artwork_fusion.background_color:
        pass
    else:
        FulfillProductCommunicationService.push_artwork(user_product_artwork, shop)
