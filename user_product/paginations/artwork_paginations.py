from collections import OrderedDict

from rest_framework.response import Response

from HUB.paginations import EnhancedPageNumberPagination
from user_product.serializers import ArtworkSizeSerializer


class ArtworkPagination(EnhancedPageNumberPagination):
    ARTWORK_SIZE_ALLOWED__FILTER_FIELDS = ('owner', 'is_active')

    def __init__(self):
        super().__init__()
        self.queryset = None
        self.options = None

    def paginate_queryset(self, queryset, request, view=None):
        self.options = self.get_options(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_options(self, queryset):
        size_options = self.get_size_options(queryset)
        options = OrderedDict([
            ("sizes", size_options)
        ])
        return options

    def get_size_options(self, queryset):
        new_queryset = self._get_new_pure_queryset(queryset, self.ARTWORK_SIZE_ALLOWED__FILTER_FIELDS)
        size_option_queryset = new_queryset.order_by("-width", "-height").values("width", "height").distinct()
        return ArtworkSizeSerializer(size_option_queryset, many=True).data

    def get_paginated_response(self, data):
        response_data_dict = super().get_paginated_response(data).data
        response_data_dict["options"] = self.options
        return Response(response_data_dict)
