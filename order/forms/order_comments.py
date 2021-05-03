import logging
from django.forms import forms

logger = logging.getLogger(__name__)


class OrderCommentsForm(forms.Form):
    content = forms.Field()
    order = forms.Field()

    class Meta:
        fields = ["content", "order"]
