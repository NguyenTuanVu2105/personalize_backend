from HUB.services.xlsx_supporter.fields.abstract_field import AbstractField


class MethodField(AbstractField):
    def __init__(self, method, **kwargs):
        super(MethodField, self).__init__(**kwargs)
        self.method = method

    def to_representation(self, instance):
        return self.method(instance)
