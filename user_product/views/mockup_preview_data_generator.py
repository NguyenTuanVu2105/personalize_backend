import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from HUB.caches import get_cached_object
from HUB.throttle import UserThrottle
from HUB.viewsets.base import BaseGenericAPIView
from abstract_product.constants import ABSTRACT_PRODUCT_MOCKUP_INFO_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.models import AbstractProduct
from abstract_product.tasks import cache_object_if_not_exist_task
from user.contants.rate_limit_views import RateLimitView
from ..forms import MockupPreviewDataForm
from ..functions import mockup_preview_data_generator
from ..models import SampleProduct, UserProduct

User = get_user_model()
logger = logging.getLogger(__name__)


class MockupPreviewDataGeneratorView(BaseGenericAPIView):
    """
        Return mockup datas
        of an abstract product for Mockup Service
    """

    error_messages = {
        "abstract_product": {
            "invalid": "This abstract_product is invalid",
        }
    }

    throttle_classes = [UserThrottle]
    throttle_view = RateLimitView.PREVIEW_MOCKUP

    def post(self, request):
        request_data = request.data
        mockup_preview_data_form = MockupPreviewDataForm(data=request_data)
        if mockup_preview_data_form.is_valid():
            try:
                product_id = str(request_data['product_id'])
                abstract_product = AbstractProduct.objects.get(pk=product_id)
                mockup_version = abstract_product.active_mockup_version
                if "original_sample_product_id" in request_data:
                    sample_product = SampleProduct.objects.get(pk=request_data['original_sample_product_id'])
                    mockup_version = sample_product.mockup_version
                elif "original_user_product_id" in request_data:
                    user_product = UserProduct.objects.get(pk=request_data['original_user_product_id'])
                    mockup_version = user_product.mockup_version

                cache_key = ABSTRACT_PRODUCT_MOCKUP_INFO_CACHE_KEY_PREFIX + product_id + "_" + mockup_version
                cached_object = get_cached_object(cache_key)

                if cached_object:
                    return Response({"success": True, "data": cached_object})
                else:
                    data = mockup_preview_data_generator(request_data['product_id'], mockup_version)
                    cache_object_if_not_exist_task.delay(cache_key, data, ABSTRACT_PRODUCT_CACHE_TIMEOUT)
                    return Response({"success": True, "data": data})

            except AbstractProduct.DoesNotExist:
                return Response({"success": False, "message": self.error_messages['abstract_product']['invalid']})

            except Exception as e:
                logger.exception(e)
                return Response({"success": False, "message": str(e)})

        else:
            return Response(ValidationError(code="user_product", message=mockup_preview_data_form.errors))
