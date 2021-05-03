import logging

import django_filters

from HUB.filters import BaseUpdatedTimeFilter, BaseCreatedTimeFilter
from user_product.models import Artwork

logger = logging.getLogger(__name__)


class MultiSizeValuesFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        result = Artwork.objects.none()
        for v in values:
            splited_size = v.split('x')
            tmp_queryset = qs.filter(width=splited_size[0], height=splited_size[1])
            result = result | tmp_queryset

        return result


class CreatedTimeArtworkFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = Artwork


class ArtworkFilter(CreatedTimeArtworkFilter):
    size = MultiSizeValuesFilter()

    class Meta(BaseUpdatedTimeFilter.Meta):
        model = Artwork
        fields = BaseUpdatedTimeFilter.Meta.fields + ('is_public', 'status', 'size')
