from django.db.models import Q, Count

from user_product.constants import ArtworkStatus
from user_product.models import Artwork


def calculate_artwork_used_time():
    artwork_qs = Artwork.objects.all().select_related("owner").filter(
        ~Q(status=ArtworkStatus.UPLOADED) or ~Q(status=ArtworkStatus.ERROR))
    for artwork in artwork_qs:
        total_created_product = artwork.fusion_info.aggregate(Count('frame__user_product_artwork_fusion_set'))
        artwork.total_created_product = total_created_product['frame__user_product_artwork_fusion_set__count']

    Artwork.objects.bulk_update(artwork_qs, ['total_created_product'])
