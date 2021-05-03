import logging

import django_filters
from django_filters import FilterSet

from ..models import UserFontFamily

logger = logging.getLogger(__name__)


class AdminFontFilter(FilterSet):
    owner = django_filters.Filter(method="owner_filter")
    status = django_filters.Filter(method="status_filter")

    @staticmethod
    def owner_filter(qs, value, *args):
        if args[0] == '0':
            return qs.filter(owner__isnull=True)
        else:
            return qs.filter(owner=args[0])

    @staticmethod
    def status_filter(qs, value, *args):
        if args[0] == '1':
            return qs.filter(is_active=True)
        elif args[0] == '2':
            return qs.filter(is_active=False)
        else:
            return qs

    class Meta:
        model = UserFontFamily
        fields = ('status', 'owner')
