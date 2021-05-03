from user_product.models.artwork_history import ArtworkHistory


def create_artwork_history(original_artwork_id, original_name, original_image_url, original_width, original_height,
                           sha256):
    ArtworkHistory.objects.create(original_artwork_id=original_artwork_id,
                                  original_name=original_name,
                                  original_image_url=original_image_url,
                                  original_width=original_width,
                                  original_height=original_height, sha256=sha256)
