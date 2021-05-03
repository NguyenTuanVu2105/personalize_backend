import logging

from celery.decorators import task

from HUB.constants.celery_task import CeleryTask
from user_product.models import UserProduct, UserVariantSideMockup
from .sync_product_in_shop import create_product_in_shop_task, update_product_in_shop_task

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_PROCESS_NO_ARTWORK_PRODUCT)
def process_no_artwork_user_product_task(user_product_id, is_created=True):
    user_product = UserProduct.objects.get(pk=user_product_id)
    abstract_product = user_product.abstract_product
    abstract_product_mockup_infos = abstract_product.mockup_infos.all()
    active_mockup_version = abstract_product.active_mockup_version

    for abstract_product_mockup_info in abstract_product_mockup_infos:
        mockup_infos = abstract_product_mockup_info.meta['mockup_infos'].get(active_mockup_version)
        for mockup_info in mockup_infos:
            for user_variant in user_product.user_product_variant_set.all():
                if user_variant.abstract_variant.mockup_info.id == abstract_product_mockup_info.id:
                    mockup_url = mockup_info['image_url']
                    mockup_thumbnail_url = mockup_info['image_url']
                    UserVariantSideMockup.objects.create(user_variant=user_variant,
                                                         mockup_url=mockup_url,
                                                         mockup_thumbnail_url=mockup_thumbnail_url)

    # first_variant = user_product.user_product_variant_set.filter(is_active=True).order_by('sort_index').first()
    # user_product.preview_image_url = first_variant.get_preview_mockup()
    first_mockup_infos = abstract_product_mockup_infos[0].meta['mockup_infos']
    user_product.preview_image_url = first_mockup_infos.get(active_mockup_version)[0]["image_url"]
    user_product.save()

    for shop_user_product in user_product.shop_user_product_set.all():
        if is_created:
            create_product_in_shop_task.delay(shop_user_product.id)
        else:
            update_product_in_shop_task.delay(shop_user_product.id)
