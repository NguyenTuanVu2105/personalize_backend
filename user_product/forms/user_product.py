from django import forms

from HUB.forms.base import ModelForm
from user_product.models import UserProduct


class UserProductForm(ModelForm):
    abstract_product_id = forms.IntegerField()
    user_product_infos = forms.Field()
    variants = forms.Field()
    shops = forms.Field()

    class Meta:
        model = UserProduct
        fields = ["abstract_product_id", "user_product_infos", "variants", "shops"]
        optional_fields = ["shops"]
