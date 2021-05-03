from django import forms


class PreviewMockupForm(forms.Form):
    product_id = forms.IntegerField()
    artwork_info = forms.Field()

    class Meta:
        fields = ["product_id", "artwork_info"]
