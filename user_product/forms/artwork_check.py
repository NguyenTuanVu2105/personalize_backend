from django import forms


class ArtworkCheckForm(forms.Form):
    sha256 = forms.Field()

    class Meta:
        fields = ["sha256"]
