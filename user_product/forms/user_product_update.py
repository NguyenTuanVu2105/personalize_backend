from HUB.forms.base import ModelForm
from helper.string_helpers import remove_unsafe_html_elements
from user_product.models import UserProduct

ALLOWED_UPDATE_FIELDS = ["title", "description"]


class UserProductUpdateForm(ModelForm):
    class Meta:
        model = UserProduct
        fields = ["id"] + ALLOWED_UPDATE_FIELDS
        optional = [ALLOWED_UPDATE_FIELDS]

    def clean_description(self):
        description = self.cleaned_data["description"]
        return remove_unsafe_html_elements(description)
