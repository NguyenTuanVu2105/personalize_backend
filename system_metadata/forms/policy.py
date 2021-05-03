from HUB.forms.base import ModelForm
from helper.string_helpers import remove_unsafe_html_elements
from system_metadata.models import Policy


class PolicyForm(ModelForm):
    class Meta:
        model = Policy
        fields = ["title", "content", "sort_index"]
        optional_fields = ["last_updated_content", "is_active", "is_prompt"]

    def clean_content(self):
        return remove_unsafe_html_elements(self.data.get("content"))

    def clean_last_updated_content(self):
        return remove_unsafe_html_elements(self.data.get("last_updated_content"))
