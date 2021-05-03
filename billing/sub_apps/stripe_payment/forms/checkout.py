from django import forms


class CheckoutForm(forms.Form):
    type = forms.Field()
    total_cost = forms.Field()
    currency = forms.Field()
    metadata = forms.Field()

    class Meta:
        fields = ["total_cost", "type", "currency", "metadata"]
