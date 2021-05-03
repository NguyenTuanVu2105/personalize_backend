from django.db.models import Q
from django_filters import Filter
from django_filters.constants import EMPTY_VALUES


class UserFieldFilter(Filter):
    def __init__(self, lookup_fields=None, *args, **kwargs):
        if lookup_fields is None:
            lookup_fields = ['id', 'email', 'name']
        self.lookup_fields = lookup_fields
        super(UserFieldFilter, self).__init__(**kwargs)

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        lookup_kwargs = Q()
        for field in self.lookup_fields:
            lookup_field = f'{self.field_name}__{field}__{self.lookup_expr}'
            lookup_kwargs = lookup_kwargs | Q(**{lookup_field: value})
        return qs.filter(lookup_kwargs)
