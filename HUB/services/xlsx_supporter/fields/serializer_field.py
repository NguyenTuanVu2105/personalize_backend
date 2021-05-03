import json

from django.db.models import F

from HUB.services.xlsx_supporter.fields.abstract_field import AbstractField


class SerializerField(AbstractField):
    def __init__(self, serializer_class, related_key, **kwargs):
        super(SerializerField, self).__init__(**kwargs)
        self.serializer_class = serializer_class
        self.related_key = related_key

    def to_representation(self, instance):
        if self.related_key:
            try:
                annotated_queryset = type(instance).objects.filter(pk=instance.pk) \
                    .annotate(**{self.related_key: F(self.related_key)})
                related_obj_id = [getattr(obj, self.related_key) for obj in annotated_queryset]
                target_model = self.serializer_class.Meta.model
                related_obj_queryset = target_model.objects.filter(pk__in=related_obj_id)
            except ValueError:
                try:
                    related_obj_queryset = getattr(instance, self.related_key).get_queryset()
                except AttributeError:
                    '''
                    getattr(instance, self.related_key) must be valid because conflict appear in annotate
                    So get_queryset is not valid                    
                    '''
                    related_obj = getattr(instance, self.related_key)
                    return dict(self.serializer_class(related_obj).data)
            ret_data = list()
            for obj in related_obj_queryset:
                data = json.dumps(self.serializer_class(obj).data, ensure_ascii=False)
                ret_data.append(data)
            return ret_data
        return dict(self.serializer_class(instance).data)
