import logging

from abstract_product.constants import AbstractType
from order.forms.order_item import SampleOrderItemForm
from order.services.order_history import create_order_history_for_order_item_remove
from user_product.constants.artwork_statuses import ArtworkStatus
from user_product.constants.user_product_status import UserProductStatus
from user_product.functions.sample_product.create_user_product import create_user_product
from user_product.functions.update_artwork_status import update_artwork_status
from user_product.models.sample_product import SampleProduct
from user_product.models.user_product import UserProduct
from user_product.models.user_variant import UserVariant

logger = logging.getLogger(__name__)


def active_user_product_by_variant(variant_id):
    user_variant = UserVariant.objects.get(pk=variant_id)
    user_product = user_variant.user_product
    if user_product and user_product.status != UserProductStatus.ACTIVE:
        user_product.status = UserProductStatus.ACTIVE
        user_product.save()
    update_artwork_status(user_product=user_product, status=ArtworkStatus.ACTIVE)


def save_order_item(items, user, order_obj, log_history=None):
    item_count = 0
    for item in items:
        if 'sample_product_id' in item:
            sample_product = SampleProduct.objects.get(pk=item['sample_product_id'])
            original_variant_sku = str(item['user_variant_id'])
            user_product = UserProduct.objects.filter(user=user, sample_product_id=item['sample_product_id']).first()
            if not user_product:
                user_product, success = create_user_product(sample_product, user)

            selected_variant = user_product.user_product_variant_set.filter(
                sample_product_variant_sku=original_variant_sku).first()

            item["user_variant_id"] = selected_variant.id
            item["id"] = selected_variant.id

        else:
            remove_old_thank_you_card(order_obj, item["user_variant_id"])
            item["user_variant_id"] = item["user_variant_id"]

        item["order"] = order_obj.pk
        item["item_id"] = item["id"]

        order_item_form = SampleOrderItemForm(data=item)
        order_item_form.validate()
        order_item = order_item_form.save()
        active_user_product_by_variant(item["user_variant_id"])
        item_count += 1

        if log_history:
            log_history(order_obj, order_item)

    return item_count


def remove_item(order_obj, order_item_obj):
    create_order_history_for_order_item_remove(order_obj=order_obj, order_item_obj=order_item_obj)
    order_pack = order_item_obj.order_pack
    order_item_obj.delete()
    if len(order_pack.items.all()) == 0:
        order_pack.delete()


def remove_old_thank_you_card(order_obj, user_variant_id):
    user_variant = UserVariant.objects.filter(id=user_variant_id).first()
    if user_variant.type == AbstractType.THANK_YOU_CARD:
        remove_items = order_obj.items.filter(
            user_variant__user_product__abstract_product__type=AbstractType.THANK_YOU_CARD)
        for item in remove_items:
            remove_item(order_obj=order_obj, order_item_obj=item)
        return None
