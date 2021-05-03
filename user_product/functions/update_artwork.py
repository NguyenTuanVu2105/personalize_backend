from user_product.constants import ArtworkStatus


def deactivate_artworks(queryset, ids):
    return bulk_update_artwork_active_status(queryset=queryset, ids=ids, new_status=ArtworkStatus.INACTIVE)


def activate_artworks(queryset, ids):
    return bulk_update_artwork_active_status(queryset=queryset, ids=ids, new_status=ArtworkStatus.ACTIVE)


def bulk_update_artwork_active_status(queryset, ids, new_status):
    # assert isinstance(new_status, bool)
    updated_row_count = queryset.filter(id__in=ids).exclude(status=new_status).update(status=new_status)
    return updated_row_count
