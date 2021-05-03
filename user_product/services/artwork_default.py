import hashlib

from PIL import Image

from HUB.services import gs_image_service
from abstract_product.models import AbstractProductSide
from user_product.functions.storage.user_image_service import artwork_default_image_service
from user_product.models import ArtworkDefault, Artwork


def upload_artwork_default(request):
    data = request.data

    side_id = data['side_id']
    side = AbstractProductSide.objects.get(pk=side_id)

    abstract_product = side.abstract_product
    imageData = request.data['image']
    image = Image.open(imageData)
    prefix = generate_prefix_name(side)
    file_url, original_image_path, thumbnail_image_path = store_image(prefix, image)
    readable_hash = hashlib.sha256(imageData.read()).hexdigest()
    return ArtworkDefault.objects.create(
        name=abstract_product.title,
        width=image.width,
        height=image.height,
        product_side=side,
        file_url=file_url,
        original_image_path=original_image_path,
        thumbnail_image_path=thumbnail_image_path,
        product_sku=abstract_product.sku,
        sha256=readable_hash
    )


def store_image(prefix, image):
    file_extension = image.format
    original_image_url, thumbnail_url = artwork_default_image_service.upload(prefix, image,
                                                                             file_extension=file_extension)
    storage_artwork_path = gs_image_service.convert_signed_url_to_file_path(original_image_url)
    storage_thumbnail_path = gs_image_service.convert_signed_url_to_file_path(thumbnail_url)

    return thumbnail_url, storage_artwork_path, storage_thumbnail_path


def generate_prefix_name(side):
    return side.type


def delete_artwork_default(artwork_default):
    remove_artwork_relations(artwork_default.id)
    artwork_default.delete()


def remove_artwork_relations(artwork_default_id):
    Artwork.objects.filter(artwork_default_id=artwork_default_id).update(artwork_default=None)


def update_artwork_default(artwork_default, request):
    data = request.data

    if 'image' in data:
        prefix = generate_prefix_name(artwork_default.product_side)
        image = Image.open(data['image'])

        file_url, original_image_path, thumbnail_image_path = store_image(prefix, image)

        artwork_default.file_url = file_url
        artwork_default.original_image_path = original_image_path
        artwork_default.thumbnail_image_path = thumbnail_image_path
        remove_artwork_relations(artwork_default.id)

    if 'name' in data:
        artwork_default.name = data['name']
    artwork_default.save()
    return artwork_default
