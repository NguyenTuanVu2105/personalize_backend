import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.helpers.error_messages import to_standard_error_messages, to_standard_error_message_by_name
from HUB.throttle import UserThrottle
from HUB.viewsets.base import BaseGenericAPIView
from abstract_product.models import AbstractProduct
from helper.string_helpers import remove_unsafe_html_elements
from shop.models import Shop
from user.contants.rate_limit_views import RateLimitView
from user_product.constants.shop_user_product_sync_status import ShopUserProductSyncStatus
from user_product.functions import create_user_variants, \
    create_user_variant_default_price
from user_product.functions import process_no_artwork_user_product_task
from user_product.models import UserProduct, ShopUserProduct
from ..forms import UserProductForm

User = get_user_model()
logger = logging.getLogger(__name__)


class NoArtworkUserVariantCreateView(BaseGenericAPIView):
    """
           View for list or create UserVariant
           Model User Variant
    """

    error_messages = {
        **to_standard_error_messages(UserProduct.ATTRIBUTE_LABELS),
        "abstract_product": {
            "invalid": "This abstract_product is invalid",
            "not_found": ""
        },
        "artwork": {
            "invalid": "This artwork is invalid",
        },
        "shop": {
            **to_standard_error_message_by_name('Shop'),
            "empty": "The shop is empty"
        },
        "abstract_variant": {
            "invalid": "This abstract_variant is invalid",
        },
        "product_side": {
            "invalid": "This product_side is invalid",
        },
        "user_variant": {
            "error": "Can not create this user_variant",
        },
        "product_side_image": {
            "invalid": "This product_side_image is invalid",
        },
        "shop_user_product": {
            "invalid": "This shop_user_product is invalid",
        }
    }

    throttle_classes = [UserThrottle]
    throttle_view = RateLimitView.CREATE_USER_PRODUCT

    def post(self, request):
        request_data = request.data

        user_product_form = UserProductForm(data=request_data)
        user_product_form.validate()
        created_user_products = []
        with transaction.atomic():
            seller_id = request.user.pk
            seller = User.objects.get(pk=request.user.pk)
            abstract_product_id = request_data['abstract_product_id']
            user_product_infos = request_data['user_product_infos']
            variants = request_data['variants']
            shops = Shop.objects.filter(owner=seller_id, id__in=request_data['shops']).values('id', 'currency')

            # if len(shops) == 0:
            #     raise FormValidationError('shop', 'invalid')

            for user_product_info in user_product_infos:
                artworks = user_product_info['artworks']
                abstract_product = AbstractProduct.objects.get(pk=abstract_product_id)
                extra_cost = abstract_product.meta.pricing_meta["extra_artwork"] * len(artworks)
                user_product = UserProduct.objects.create(user=seller,
                                                          abstract_product=abstract_product,
                                                          title=user_product_info['title'],
                                                          extra_cost=extra_cost,
                                                          preview_image_url=abstract_product.preview_image_url,
                                                          description=remove_unsafe_html_elements(
                                                              user_product_info['description']))

                created_user_products.append(user_product)
                ShopUserProduct.objects.bulk_create(map(lambda _shop: ShopUserProduct(shop_id=_shop['id'],
                                                                                      user_product_id=user_product.id,
                                                                                      sync_status=ShopUserProductSyncStatus.NEW,
                                                                                      sync_status_message=""), shops))

                create_user_variants(user_product, variants, artworks, shops)

        for created_user_product in created_user_products:
            process_no_artwork_user_product_task.delay(created_user_product.id, True)

        create_user_variant_default_price.delay(variants, seller_id)

        return Response({'success': True, "message": "Your product will appear in your shops in few minutes",
                         "product_ids": list(map(lambda p: p.id, created_user_products))})
