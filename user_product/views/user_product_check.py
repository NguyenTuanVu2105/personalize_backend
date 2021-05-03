from django.contrib.auth import get_user_model
from rest_framework.response import Response

from HUB.viewsets.base import BaseGenericAPIView
from user_product.constants.user_product_status import UserProductStatus
from user_product.models import UserProduct

User = get_user_model()


class UserProductCheckView(BaseGenericAPIView):
    def get(self, request):
        user_product_queryset = UserProduct.objects.filter(user_id=request.user.pk, status=UserProductStatus.ACTIVE)
        if len(user_product_queryset) == 0:
            return Response({"success": True, "have_product": False})
        else:
            return Response({"success": True, "have_product": True})
