from django.contrib.auth import get_user_model
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.viewsets.base import BaseGenericAPIView
from user_product.forms import ArtworkCheckForm
from ..models import Artwork

User = get_user_model()


class ArtworkCheckView(BaseGenericAPIView):
    error_messages = {
        "artwork": {
            "invalid": "This artwork is invalid",
        }
    }

    def post(self, request):
        request_data = request.data
        artwork_check_form = ArtworkCheckForm(data=request_data)
        if artwork_check_form.is_valid():
            user_artwork = Artwork.objects.filter(owner_id=request.user.pk, sha256=request_data['sha256']).first()
            if user_artwork is not None:
                return Response({"success": True, "existed": True, "artwork": user_artwork.parse_data()})
            else:
                return Response({"success": True, "existed": False})

        else:
            return Response(FormValidationError(field="artwork", code="invalid"))
