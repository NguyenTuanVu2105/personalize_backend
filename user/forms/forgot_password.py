from django import forms


class ForgotPasswordForm(forms.Form):
    email = forms.CharField()
    gRecaptcha = forms.CharField()

    class Meta:
        fields = ['email', 'gRecaptcha']
