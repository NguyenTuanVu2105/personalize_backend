from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    gRecaptcha = forms.CharField()

    class Meta:
        # model = User
        fields = ['name', 'email', 'password', 'gRecaptcha']
