from django.db.models import F

from HUB.services.xlsx_supporter.fields.abstract_field import AbstractField


class AttributeField(AbstractField):
    def __init__(self, source, aggregate=None, agg_filter=None, agg_distinct=False, **kwargs):
        super(AttributeField, self).__init__(**kwargs)
        self.source = source
        self.aggregate = aggregate
        self.agg_filter = agg_filter
        self.agg_distinct = agg_distinct

    def to_representation(self, instance):
        if hasattr(instance, self.source):
            if self.aggregate:
                '''
                    CASE: field is a ManyToManyField: 
                        - Because this field is a related object, so use Serializer instead
                '''
                raise AttributeField('Cannot aggregate {}'.format(self.source))
            else:
                return getattr(instance, self.source)
        else:
            expr = F(self.source) if not self.aggregate \
                else self.aggregate(self.source, distinct=self.agg_distinct,
                                    filter=self.agg_filter)
            queryset = type(instance).objects.annotate(**{self.source: expr}).distinct()
            representation = queryset.values(self.source).get(pk=instance.pk).get(self.source)
            return representation if representation != [None] else ''
