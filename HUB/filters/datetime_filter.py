from django_filters import FilterSet, IsoDateTimeFilter


class BaseCreatedTimeFilter(FilterSet):
    since = IsoDateTimeFilter(field_name="create_time", lookup_expr='gte')
    until = IsoDateTimeFilter(field_name="create_time", lookup_expr='lte')

    class Meta:
        model = None
        fields = ('since', 'until',)


class BaseUpdatedTimeFilter(BaseCreatedTimeFilter):
    since = IsoDateTimeFilter(field_name="update_time", lookup_expr='gte')
    until = IsoDateTimeFilter(field_name="update_time", lookup_expr='lte')

    class Meta(BaseCreatedTimeFilter.Meta):
        pass
