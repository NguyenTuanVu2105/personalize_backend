from django import forms


class BackgroundCustomizeDataForm(forms.Form):
    product_id = forms.IntegerField()

    class Meta:
        fields = ["product_id"]
