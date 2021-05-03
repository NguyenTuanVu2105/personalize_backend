from django import forms


class MockupPreviewDataForm(forms.Form):
    product_id = forms.IntegerField()

    class Meta:
        fields = ["product_id"]
