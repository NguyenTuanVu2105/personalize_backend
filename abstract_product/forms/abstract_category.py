from django import forms


class AbstractCategoryForm(forms.Form):
    title = forms.CharField()
    product_list = forms.Field()

    class Meta:
        fields = ['title', 'product_list']
