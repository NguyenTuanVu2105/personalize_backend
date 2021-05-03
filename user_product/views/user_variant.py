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
from shop.constants.shop_status import ShopStatus
from shop.models import Shop
from user.contants.rate_limit_views import RateLimitView
from user_product.constants import MAX_SCALE_ALLOW
from user_product.constants.shop_user_product_sync_status import ShopUserProductSyncStatus
from user_product.functions import create_artworks_and_relations, create_user_variants, \
    create_user_variant_default_price
from user_product.models import UserProduct, ShopUserProduct, UserVariantSideMockup
from ..forms import UserProductForm
from ..functions.artwork_fusion.generate_artwork_fusion import generate_product_artwork_fusion
from ..functions.artwork_fusion.regenerate_user_product_artwork_fusion import generate_product_combined_artwork_fusion
from ..functions.sync_product_in_shop.sync_tasks import sync_user_product

User = get_user_model()
logger = logging.getLogger(__name__)


class UserVariantCreateView(BaseGenericAPIView):
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
            "large_scale": "This artwork is scale too large",
            "position": "This artwork has invalid drag position"
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
        },

    }

    throttle_classes = [UserThrottle]
    throttle_view = RateLimitView.CREATE_USER_PRODUCT

    def post(self, request):
        request_data = request.data
        logger.info(f'Publish product for user: {request.user.pk}')

        user_product_form = UserProductForm(data=request_data)
        user_product_form.validate()
        created_user_products = []

        with transaction.atomic():
            seller_id = request.user.pk
            abstract_product_id = request_data['abstract_product_id']
            user_product_infos = request_data['user_product_infos']
            variants = request_data['variants']

            shops = Shop.objects.filter(owner=seller_id, id__in=request_data['shops'], status=ShopStatus.ACTIVE).values(
                'id', 'currency')

            user_products_to_create = []
            for user_product_info in user_product_infos:
                side_layers = user_product_info['sideLayers']
                user_product_mockups = user_product_info['userProductMockups']
                abstract_product = AbstractProduct.objects.select_related('meta').only('id', 'meta__pricing_meta').get(
                    pk=abstract_product_id)

                for artwork in side_layers:
                    layers = artwork['layers']
                    for layer in layers:
                        dnd_scale = layer['dndScale']
                        if dnd_scale > MAX_SCALE_ALLOW:
                            raise FormValidationError('layer', 'large_scale')

                not_empty_sides = list(filter(lambda s: len(s['layers']) != 0, side_layers))
                extra_cost = abstract_product.meta.pricing_meta["extra_artwork"] * max(0, len(not_empty_sides) - 1)
                user_products_to_create.append(UserProduct(user_id=seller_id,
                                                           abstract_product_id=abstract_product.id,
                                                           title=user_product_info['title'],
                                                           extra_cost=extra_cost,
                                                           mockup_version=abstract_product.active_mockup_version,
                                                           description=remove_unsafe_html_elements(
                                                               user_product_info['description'])))

            created_user_products = UserProduct.objects.bulk_create(user_products_to_create)

            shop_user_products_to_create = []
            for index, user_product_info in enumerate(user_product_infos):
                user_product = created_user_products[index]
                for shop in shops:
                    shop_user_products_to_create.append(ShopUserProduct(shop_id=shop['id'],
                                                                        user_product=created_user_products[index],
                                                                        sync_status=ShopUserProductSyncStatus.NEW,
                                                                        sync_status_message=""))

                create_artworks_and_relations(user_product, side_layers, seller_id)
                create_user_variants(user_product, variants, side_layers, shops)

            ShopUserProduct.objects.bulk_create(shop_user_products_to_create)
            user_variants = user_product.user_product_variant_set.filter(mockup_per_side__isnull=True)

            for user_product_mockup in user_product_mockups:
                is_aop_mockup = user_product_mockup['isAOPMockup']
                if is_aop_mockup:
                    for user_variant in user_variants:
                        if user_variant.abstract_variant.mockup_info.id == user_product_mockup['mockup_info_id']:
                            variant_mockup_image_url = user_product_mockup['original']
                            UserVariantSideMockup.objects.create(user_variant=user_variant,
                                                                 mockup_url=variant_mockup_image_url,
                                                                 mockup_thumbnail_url=variant_mockup_image_url)
                else:
                    for user_variant in user_variants:
                        if user_variant.abstract_variant.get_color_value() == user_product_mockup['color']:
                            variant_mockup_image_url = user_product_mockup['original']
                            UserVariantSideMockup.objects.create(user_variant=user_variant,
                                                                 mockup_url=variant_mockup_image_url,
                                                                 mockup_thumbnail_url=variant_mockup_image_url)

            first_variant = user_product.user_product_variant_set.filter(is_active=True).order_by('sort_index').first()
            user_product.preview_image_url = first_variant.get_preview_mockup()
            user_product.save()

        for created_user_product in created_user_products:
            sync_user_product(created_user_product)
            user_product_artworks = user_product.artwork_set.all()
            combine_fusion = user_product.combine_fusion
            if not combine_fusion:
                for user_product_artwork_fusion in user_product_artworks:
                    generate_product_artwork_fusion(user_product_artwork_fusion)
            else:
                fulfill_user_product_artwork_fusion = user_product_artworks.send_to_fulfill_filter().first()
                separated_side_user_product_artwork_fusions = user_product_artworks.send_to_fulfill_exclude()
                generate_product_combined_artwork_fusion(user_product, separated_side_user_product_artwork_fusions,
                                                         fulfill_user_product_artwork_fusion)

        create_user_variant_default_price.delay(variants, seller_id)

        return Response({'success': True, "message": "Your product will appear in your shops in few minutes",
                         "product_ids": list(map(lambda p: p.id, created_user_products))})
