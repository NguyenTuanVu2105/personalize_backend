import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from HUB.viewsets.base import BaseGenericAPIView
from abstract_product.models import AbstractProduct, AbstractProductMockupInfo
from ..forms import BackgroundCustomizeDataForm

User = get_user_model()
logger = logging.getLogger(__name__)


class BackgroundCustomizeDataGeneratorView(BaseGenericAPIView):
    error_messages = {
        "abstract_product": {
            "invalid": "This abstract_product is invalid",
        }
    }

    # throttle_classes = [UserThrottle]
    # throttle_view = RateLimitView.PREVIEW_MOCKUP

    def post(self, request):
        request_data = request.data
        bg_customize_data_form = BackgroundCustomizeDataForm(data=request_data)
        if bg_customize_data_form.is_valid():
            try:
                product_id = request_data['product_id']
                abstract_product = AbstractProduct.objects.get(id=product_id)
                active_mockup_version = abstract_product.active_mockup_version
                response_data = []
                for mockup_info in AbstractProductMockupInfo.objects.filter(abstract_product_id=product_id):
                    mockup_meta = mockup_info.meta
                    # logger.info(active_mockup_version)
                    for mockup in mockup_meta['mockup_infos'].get(active_mockup_version, []):
                        if 'side' in mockup and 'mask' in mockup:
                            response_data.append({
                                "side": mockup['side'],
                                "mask_path": mockup['mask'],
                                "consistency_name": mockup_meta['consistency_name']
                            })

                return Response({"success": True, "data": response_data})

            except AbstractProduct.DoesNotExist:
                return Response({"success": False, "message": self.error_messages['abstract_product']['invalid']})

            except Exception as e:
                logger.exception(e)
                return Response({"success": False, "message": str(e)})

        else:
            return Response(ValidationError(code="user_product", message=bg_customize_data_form.errors))
