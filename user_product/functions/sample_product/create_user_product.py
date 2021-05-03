import logging
import traceback

from django.db import transaction
from django.db.models.functions import Now

from user_product.constants import ArtworkStatus, UserProductStatus
from user_product.forms import TextPersonalizationForm
from user_product.models import UserProduct, UserVariant, UserVariantPrice, UserProductArtworkFusion, \
    UserVariantSideMockup, Artwork, ArtworkFusionInfo, ArtworkFusion, ArtworkDefault

logger = logging.getLogger(__name__)


def create_user_product(sample_product, user):
    try:
        with transaction.atomic():
            sample_product_data = sample_product.detail_data
            # logger.info("Creating user product: {}".format(sample_product_data['title']))
            created_user_product = UserProduct.objects.create(user=user, title=sample_product_data['title'],
                                                              extra_cost=sample_product_data['extra_cost'],
                                                              description=sample_product_data['description'],
                                                              abstract_product_id=sample_product_data[
                                                                  'abstract_product'],
                                                              preview_image_url=sample_product_data[
                                                                  'preview_image_url'],
                                                              status=UserProductStatus.UNUSED,
                                                              is_updated_fusions=True,
                                                              sample_product=sample_product)

            user_variant_datas = sample_product_data['user_variant_data']
            for user_variant_data in user_variant_datas:
                create_user_variant(user_variant_data, created_user_product)

            user_product_artwork_fusion_datas = sample_product_data['user_product_artwork_fusion_data']
            for user_product_artwork_fusion_data in user_product_artwork_fusion_datas:
                create_artwork_relations(user_product_artwork_fusion_data, created_user_product, user)

            return created_user_product, True

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
        return None, False


def create_user_variant(user_variant_data, created_user_product):
    # logger.info("Creating user variant: {}".format(user_variant_data['abstract_variant']))
    created_user_variant = UserVariant.objects.create(user_product=created_user_product, is_active=True,
                                                      sort_index=user_variant_data['sort_index'],
                                                      sample_product_variant_sku=user_variant_data['sku'],
                                                      abstract_variant_id=user_variant_data[
                                                          'abstract_variant'])
    created_user_variant.sku = created_user_variant.id
    created_user_variant.save()

    user_variant_price_datas = user_variant_data['user_variant_price_data']
    user_variant_prices_to_create = []
    for user_variant_price_data in user_variant_price_datas:
        # logger.info("Appending user variant price: {}".format(user_variant_price_data['value']))
        user_variant_prices_to_create.append(UserVariantPrice(user_variant=created_user_variant,
                                                              value=user_variant_price_data['value'],
                                                              currency=user_variant_price_data['currency']))
    UserVariantPrice.objects.bulk_create(user_variant_prices_to_create)

    user_variant_side_mockup_datas = user_variant_data['user_variant_side_mockup_data']
    user_variant_side_mockups_to_create = []
    for user_variant_side_mockup_data in user_variant_side_mockup_datas:
        # logger.info("Appending user variant side mockup: {}".format(user_variant_side_mockup_data[
        #                                                                 'mockup_url']))
        user_variant_side_mockups_to_create.append(UserVariantSideMockup(user_variant=created_user_variant,
                                                                         mockup_thumbnail_url=
                                                                         user_variant_side_mockup_data[
                                                                             'mockup_thumbnail_url'],
                                                                         mockup_url=
                                                                         user_variant_side_mockup_data[
                                                                             'mockup_url']))
    UserVariantSideMockup.objects.bulk_create(user_variant_side_mockups_to_create)


def create_artwork_relations(user_product_artwork_fusion_data, created_user_product, user):
    # logger.info("Creating user product artwork fusion with size: {}".format(
    #     user_product_artwork_fusion_data['product_side']))

    created_user_product_artwork_fusion = UserProductArtworkFusion.objects.create(
        product_side_id=user_product_artwork_fusion_data['product_side'], user_product=created_user_product,
        send_to_fulfill=user_product_artwork_fusion_data['send_to_fulfill'])

    artwork_fusion_data = user_product_artwork_fusion_data['artwork_fusion']
    # logger.info("Creating artwork fusion: {}".format(artwork_fusion_data['name']))
    created_artwork_fusion = ArtworkFusion.objects.create(name=artwork_fusion_data['name'], owner=user,
                                                          image_url=artwork_fusion_data['image_url'],
                                                          background_color=artwork_fusion_data[
                                                              'background_color'],
                                                          original_image_path=artwork_fusion_data[
                                                              'original_image_path'])

    artwork_fusion_info_datas = artwork_fusion_data['artwork_fusion_info_data']
    for artwork_fusion_info_data in artwork_fusion_info_datas:
        # logger.info("Creating artwork fusion info with layer: {}".format(artwork_fusion_info_data['layer']))
        created_artwork_fusion_info = ArtworkFusionInfo.objects.create(frame=created_artwork_fusion,
                                                                       layer=artwork_fusion_info_data[
                                                                           'layer'],
                                                                       scale=artwork_fusion_info_data[
                                                                           'scale'],
                                                                       position=artwork_fusion_info_data[
                                                                           'position'],
                                                                       rotation=artwork_fusion_info_data[
                                                                           'rotation'],
                                                                       dnd_scale=artwork_fusion_info_data[
                                                                           'dnd_scale'])

        layer_content_data = artwork_fusion_info_data['layer_content']
        created_layer = create_layer_content(layer_content_data, user)

        created_artwork_fusion_info.layer_content = created_layer
        created_artwork_fusion_info.save()

    # logger.info("Updating artwork fusion for user product artwork fusion: {}".format(
    #     created_user_product_artwork_fusion.product_side_id))
    created_user_product_artwork_fusion.artwork_fusion = created_artwork_fusion
    created_user_product_artwork_fusion.save()


def create_layer_content(layer_content_data, user):
    if 'raw_svg' in layer_content_data:
        text_personalization_form = TextPersonalizationForm(
            data={**layer_content_data, "font_family": layer_content_data['font_family']['id']})
        text_personalization_form.validate()
        text_personalization = text_personalization_form.save()

        return text_personalization

    else:
        artwork_field_to_update = {
            "name": layer_content_data['name'],
            "width": layer_content_data['width'],
            "height": layer_content_data['height'],
            "file_url": layer_content_data['file_url'],
            "last_used_time": Now(),
            "artwork_default_id": get_artwork_default_id(layer_content_data['artwork_default']),
            "sha256": layer_content_data['sha256'],
        }
        # logger.info("Creating artwork with sha256: {}".format(artwork_data['sha256']))
        artwork_check = Artwork.objects.filter(owner=user,
                                               original_image_path=layer_content_data[
                                                   'original_image_path'],
                                               thumbnail_image_path=layer_content_data[
                                                   'thumbnail_image_path'])

        if len(artwork_check) == 0:
            created_artwork, created = Artwork.objects.update_or_create(owner=user,
                                                                        original_image_path=layer_content_data[
                                                                            'original_image_path'],
                                                                        thumbnail_image_path=layer_content_data[
                                                                            'thumbnail_image_path'],
                                                                        status=ArtworkStatus.SP_CLONED,
                                                                        total_created_product=1,
                                                                        defaults=artwork_field_to_update)

        elif len(artwork_check) == 1:
            created_artwork, created = Artwork.objects.update_or_create(owner=user,
                                                                        original_image_path=layer_content_data[
                                                                            'original_image_path'],
                                                                        thumbnail_image_path=layer_content_data[
                                                                            'thumbnail_image_path'],
                                                                        defaults=artwork_field_to_update)
            if created:
                created_artwork.total_created_product = 1
            else:
                created_artwork.total_created_product = created_artwork.total_created_product + 1
            created_artwork.save()

        else:
            created_artwork = artwork_check.last()
            created_artwork.total_created_product = created_artwork.total_created_product + 1
            created_artwork.save()

        return created_artwork


def get_artwork_default_id(artwork_default_id):
    if ArtworkDefault.objects.filter(id=artwork_default_id).exists():
        return artwork_default_id
    else:
        return None
