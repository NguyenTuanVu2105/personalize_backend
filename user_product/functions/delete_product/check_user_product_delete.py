from user_product.constants import ShopUserProductSyncStatus, UserProductStatus


def check_user_product_delete(shop_user_product):
    user_product = shop_user_product.user_product
    change_product_delete_in_all_shop(user_product)


def change_product_delete_in_all_shop(user_product):
    for shop_user_product in user_product.shop_user_product_set.all():
        if shop_user_product.sync_status not in [ShopUserProductSyncStatus.DELETED, ShopUserProductSyncStatus.ERROR]:
            return
    user_product.status = UserProductStatus.INACTIVE
    user_product.save()
