from shop.models import Shop
from user_product.constants import ShopUserProductSyncStatus
from user_product.functions.sync_product_in_shop.create_product import create_product_in_shop
from user_product.models import ShopUserProduct, UserProduct


def bulk_resync_product(user_product_id, shop_ids):
    user_product = UserProduct.objects.get(id=user_product_id)
    for shop_id in shop_ids:
        for shop_user_product in ShopUserProduct.objects.filter(shop_id=shop_id, user_product=user_product):
            shop_user_product.is_active = False
            shop_user_product.save()
        shop = Shop.objects.get(id=shop_id)
        shop_user_product = ShopUserProduct.objects.create(shop=shop, user_product=user_product,
                                                           sync_status=ShopUserProductSyncStatus.SYNCING)
        create_product_in_shop(shop_user_product)