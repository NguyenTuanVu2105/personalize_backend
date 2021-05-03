from django import forms


class UserStripeForm(forms.Form):
    token = forms.Field()
    type = forms.Field()

    class Meta:
        fields = ["token", "type"]
