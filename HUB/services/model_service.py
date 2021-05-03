from django.db.models import F, Sum, Count

from HUB.services.xlsx_supporter.fields import AttributeField

AGGREGATE_FUNCTION_DICT = {
    'sum': Sum,
    'count': Count
}


def get_model_related_fields(instance, related_field_name, aggregate=None, agg_filter=None, agg_distinct=False):
    if hasattr(instance, related_field_name):
        if aggregate:
            raise AttributeField('Cannot aggregate {}'.format(related_field_name))
        else:
            return getattr(instance, related_field_name)
    else:
        expr = F(related_field_name) if not aggregate \
            else aggregate(related_field_name, distinct=agg_distinct,
                           filter=agg_filter)
        queryset = type(instance).objects.annotate(**{'_': expr}).distinct()
        return queryset.values('_').get(pk=instance.pk).get('_')
