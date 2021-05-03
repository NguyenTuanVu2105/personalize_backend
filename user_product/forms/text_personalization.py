import logging

from HUB.forms.base import ModelForm
from user_product.models import TextPersonalization

logger = logging.getLogger(__name__)


class TextPersonalizationForm(ModelForm):
    class Meta:
        model = TextPersonalization
        fields = ["placeholder_label", "raw_svg", "text", "font_family", "is_allow_customize", "text_color",
                  "text_size", "text_spacing", "outline_color", "outline_thickness", "shadow_color", "shadow_distance",
                  "shadow_angle", "arc"]
