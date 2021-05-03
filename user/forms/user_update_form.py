from HUB.forms.base import ModelForm
from user.models import User


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["name", "gender", "address", "birthday", "phone_number"]
        optional_fields = ["name", "gender", "address", "birthday", "phone_number"]
