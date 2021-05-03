from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from django.http import HttpResponse
from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.models import AbstractProduct
from user_product.services.user_product import UserProductService


class AdminProduct(ListModelMixin, AdminGenericViewSet):
    queryset = AbstractProduct.objects.filter(is_active=True)

    @action(methods=["GET"], detail=False, url_path="get_xlsx")
    def get_xlsx(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=test.xlsx"
        UserProductService().get_xlsx(self.queryset, response)
        return response
