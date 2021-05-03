import csv
import io
import traceback

from django.db.models import Case, When, Value, IntegerField
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AuthenticatedGenericViewSet
from service_communication.services.fulfill_services.fulfill_statistic_communication_service import \
    FulfillStatisticCommunicationService
from statistic.models import AbstractProductStatistic
from statistic.serializers.product_statistic_serializers import ProductStatisticSerializer
from statistic.functions.update_from_dict import update_production_statistics
from statistic.functions.import_from_csv import import_production_statistic_from_csv


class ProductStatisticViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
                              ListModelMixin, AuthenticatedGenericViewSet):
    queryset = AbstractProductStatistic.objects.order_by('sort_index').order_by('id')
    serializer_class = ProductStatisticSerializer

    @method_permission_required(get_permissions(['admin_statistic_update', ]))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_statistic_update', ]))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_statistic_update', ]))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(methods=["GET"], detail=False, url_path='all')
    def get_all(self, request):
        data = self.queryset.annotate(search_type_ordering=Case(
            When(production_time_default__gt=0, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )).order_by('-search_type_ordering', 'production_time_default')
        return Response(ProductStatisticSerializer(data, many=True).data)

    @action(methods=["POST"], detail=False, url_path='import',
            permission_classes=get_permissions(['admin_statistic_update']))
    def import_production_statistic(self, request):
        try:
            file = request.FILES.getlist('csv_files')[0]
            if not file.name.endswith(".csv"):
                return Response({"success": False, "message": "This is not csv file!"})
            dataset = file.read().decode('utf-8')
            io_string = io.StringIO(dataset)
            decoded_file = csv.reader(io_string, delimiter=',')
            import_production_statistic_from_csv(decoded_file)

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True, "message": "Import production statistics successfully"})

    @action(methods=["PUT"], detail=False, url_path='update',
            permission_classes=get_permissions(['admin_statistic_update']))
    def update_production_statistic(self, request):
        response = FulfillStatisticCommunicationService.get_production_statistic()
        if response['success']:
            update_production_statistics(dictData=response['data'])
            return Response({'success': True})
        return Response({'success': False})
