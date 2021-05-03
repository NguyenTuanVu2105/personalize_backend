from collections import OrderedDict
from rest_framework.response import Response
from HUB.paginations import EnhancedPageNumberPagination
from user.models import UserTag


class UserAdministrationPagination(EnhancedPageNumberPagination):
    OPTION_ALLOWED_FILTER_FIELDS = ['is_staff']

    def __init__(self):
        super().__init__()
        self.queryset = None
        self.options = None

    def paginate_queryset(self, queryset, request, view=None):
        self.options = self.get_options(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_options(self, queryset):
        option_filter_fields = ['account_type', 'is_active', 'is_email_confirmed',
                                'is_staff', 'is_superuser', 'is_valid_payment']
        options = OrderedDict([(x, self.get_distinct_value(queryset, x)) for x in option_filter_fields])
        options['tags'] = UserTag.objects.values_list('tag', flat=True).distinct().order_by()
        return options

    def get_distinct_value(self, queryset, field):
        new_queryset = self._get_new_pure_queryset(queryset, self.OPTION_ALLOWED_FILTER_FIELDS)
        return new_queryset.values_list(field, flat=True).distinct().order_by()

    def get_paginated_response(self, data):
        response_data_dict = super().get_paginated_response(data).data
        response_data_dict["options"] = self.options
        return Response(response_data_dict)
