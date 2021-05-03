from django import forms


class VerifyStoreForm(forms.Form):
    query_string = forms.CharField()

    class Meta:
        fields = ["query_string"]
