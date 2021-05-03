import logging

from celery.decorators import task
from django.contrib.auth import get_user_model

from HUB.constants.celery_task import CeleryTask
from shop.models import Shop
from user_product.constants.shop_user_product_sync_status import ShopUserProductSyncStatus
from user_product.models import ShopUserProduct, UserProduct
from .create_product import create_product_in_shop, sync_product_in_shop
from .update_product import update_product_in_shop
from ..delete_product.delete_product_in_shop import delete_product_in_shop

logger = logging.getLogger(__name__)
User = get_user_model()


def sync_user_product(user_product, is_created=True):
    for shop_user_product in user_product.shop_user_product_set.all():
        if is_created:
            create_product_in_shop_task.delay(shop_user_product.id)
        else:
            update_product_in_shop_task.delay(shop_user_product.id)


@task(name=CeleryTask.TASK_CREATE_PRODUCT_IN_SHOP)
def create_product_in_shop_task(shop_user_product_id):
    shop_user_product = ShopUserProduct.objects.get(pk=shop_user_product_id)
    # logger.info("create_product_in_shop_task...")
    shop_user_product.sync_status = ShopUserProductSyncStatus.SYNCING
    shop_user_product.save()
    create_product_in_shop(shop_user_product)


@task(name=CeleryTask.TASK_SYNC_SHOP_USER_PRODUCT_FROM_OTHERS)
def sync_product_in_shop_task(shop_user_product_id):
    shop_user_product = ShopUserProduct.objects.get(pk=shop_user_product_id)
    # logger.info("sync_product_in_shop_task...")
    shop_user_product.sync_status = ShopUserProductSyncStatus.SYNCING
    shop_user_product.save()
    sync_product_in_shop(shop_user_product)


@task(name=CeleryTask.TASK_UPDATE_PRODUCT_IN_SHOP)
def update_product_in_shop_task(shop_user_product_id):
    shop_user_product = ShopUserProduct.objects.get(pk=shop_user_product_id)
    # logger.info("update_product_in_shop_task...")
    shop_user_product.sync_status = ShopUserProductSyncStatus.SYNCING
    shop_user_product.save()
    update_product_in_shop(shop_user_product)


@task(name=CeleryTask.TASK_UPDATE_ALL_PRODUCT_IN_SHOP)
def update_all_product_in_shop(shop_id):
    shop = Shop.objects.get(pk=shop_id)
    for shop_user_product in shop.user_product_set.all():
        shop_user_product.sync_status = ShopUserProductSyncStatus.SYNCING
        shop_user_product.save()
        if shop_user_product.handle is None:
            create_product_in_shop(shop_user_product)
        else:
            update_product_in_shop(shop_user_product)


@task(name=CeleryTask.TASK_UPDATE_USER_PRODUCT_IN_ALL_SHOP)
def update_user_product_in_all_shop_task(user_product_id):
    user_product = UserProduct.objects.get(pk=user_product_id)
    for shop_user_product in user_product.shop_user_product_set.all():
        update_product_in_shop(shop_user_product)


@task(name=CeleryTask.TASK_DELETE_USER_PRODUCT_IN_SHOP)
def delete_user_product_in_shop(shop_user_product_id):
    shop_user_product = ShopUserProduct.objects.get(pk=shop_user_product_id)
    # logger.info("delete_product_in_shop_task...")
    shop_user_product.sync_status = ShopUserProductSyncStatus.DELETING
    shop_user_product.save()
    delete_product_in_shop(shop_user_product)
