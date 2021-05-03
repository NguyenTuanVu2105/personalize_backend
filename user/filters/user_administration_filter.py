from django.contrib.postgres.aggregates import ArrayAgg

from HUB import logger
from HUB.filters import BaseCreatedTimeFilter
import django_filters
from user.models import User, UserTag


class UserAdministrationFilter(BaseCreatedTimeFilter):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    id = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    tags = django_filters.CharFilter(method='filter_tags')

    @staticmethod
    def filter_tags(queryset, value, *args, **kwargs):
        try:
            if args:
                temp = UserTag.objects.values('user').annotate(tags=ArrayAgg('tag')).order_by()
                user_id = [item['user'] for item in temp if
                           all([tag_value in item['tags'] for tag_value in args[0].split(',')])]
                queryset = queryset.filter(id__in=user_id)
        except Exception as e:
            logger.info(str(e))
            return queryset.none()
        return queryset

    class Meta:
        model = User
        fields = BaseCreatedTimeFilter.Meta.fields + (
            'account_type', 'is_active', 'is_email_confirmed', 'tags',
            'is_staff', 'is_superuser', 'is_valid_payment', 'is_test_user', 'is_lock')
