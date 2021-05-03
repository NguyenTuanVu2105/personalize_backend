import csv
import io

from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin, \
    CreateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.constants import PRODUCT_SUPPLIER_CHOICES
from abstract_product.filters.supplied_product_sku_mapping import SuppliedProductSkuMappingFilter
from abstract_product.functions import import_sku_mapping_form_csv
from abstract_product.models.ffm_product_infos import FFMProductInfo
from abstract_product.serializers import FFMProductInfoSerializer
from abstract_product.services import SuppliedProductMappingWorkbook


class FFMProductInfoViewSet(AdminGenericViewSet, RetrieveModelMixin, ListModelMixin, DestroyModelMixin,
                            UpdateModelMixin, CreateModelMixin):
    queryset = FFMProductInfo.objects.all()
    serializer_class = FFMProductInfoSerializer
    filterset_class = SuppliedProductSkuMappingFilter

    def create(self, request, *args, **kwargs):
        request_data = request.data
        supplier = request_data.get('supplier')
        ph_sku = request_data.get('ph_product_sku')
        supplier_sku = request_data.get('supplier_product_sku')
        existed = self.get_queryset().filter(supplier=supplier, ph_product_sku=ph_sku,
                                             supplier_product_sku=supplier_sku).count() > 0
        if existed:
            return Response({'success': False, 'message': 'Record is already existed'})
        return super(FFMProductInfoViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        data = super(FFMProductInfoViewSet, self).list(request, *args, **kwargs).data
        data['options'] = {'suppliers': PRODUCT_SUPPLIER_CHOICES}
        return Response(data)

    @action(methods=['POST'], detail=False, url_path='import')
    def import_from_csv(self, request):
        file = request.FILES.getlist('csv_files')[0]
        if not file.name.endswith(".csv"):
            return Response({"success": False, "message": "This is not csv file!"})
        dataset = file.read().decode('utf-8')
        io_string = io.StringIO(dataset)
        decoded_file = csv.reader(io_string, delimiter=',')
        num_new_created, num_existed, num_invalid = import_sku_mapping_form_csv(decoded_file)

        return Response({'success': True, 'num_new_created': num_new_created, 'num_existed': num_existed,
                         'num_invalid': num_invalid})

    @action(methods=['get'], detail=False, url_path='export')
    def export_as_xlsx(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        workbook = SuppliedProductMappingWorkbook(queryset)
        response = workbook.get_workbook()
        return response
