from django import forms


class InitStoreForm(forms.Form):
    shop = forms.CharField()
    code = forms.CharField()
    hmac = forms.CharField()
    timestamp = forms.CharField()

    class Meta:
        fields = ["shop", "code", "hmac", "timestamp"]
