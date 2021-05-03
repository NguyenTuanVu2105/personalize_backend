from HUB.services.xlsx_supporter.fields import AttributeField


class DatetimeField(AttributeField):
    def to_representation(self, instance):
        return str(super(DatetimeField, self).to_representation(instance))
