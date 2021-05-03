from user_product.constants import ShopUserProductSyncStatus
from user_product.models import UserProduct, ShopUserProduct


def create_user_product_from_ecomerce_product(ecommerce_product, user_id):
    try:
        product = ecommerce_product.product_meta
        user_product = UserProduct.objects.create(user_id=user_id,
                                                  preview_image_url=product['image']['src'],
                                                  title=product['title'],
                                                  description=product['body_html'],
                                                )
        ShopUserProduct.objects.create(shop=ecommerce_product.shop, user_product=user_product, sync_status=ShopUserProductSyncStatus.SYNCED, sync_status_message="")
        ecommerce_product.user_product_mapping = user_product
        ecommerce_product.save()
    except Exception:
        raise Exception
    else:
        return user_product