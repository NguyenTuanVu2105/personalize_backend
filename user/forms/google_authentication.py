from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class GAuthenticationForm(forms.Form):
    id_token = forms.CharField()
    access_token = forms.CharField()

    class Meta:
        # model = User
        fields = ['access_token', 'id_token']
