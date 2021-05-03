import csv
import io
import logging
import traceback

from rest_framework.response import Response

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericAPIView
from abstract_product.functions import import_from_csv, sync_artwork_default
from abstract_product.tasks import cache_abstract_category_products_task, cache_abstract_products_task

logger = logging.getLogger(__name__)


class ProductDataImport(AdminGenericAPIView):

    @method_permission_required(get_permissions(['admin_product_data_import',]))
    def post(self, request):
        try:
            deactivate = request.data.get('deactivate')
            deactivate = deactivate is None or deactivate.lower() != 'false'
            file = request.FILES.getlist('csv_files')[0]
            if not file.name.endswith(".csv"):
                return Response({"success": False, "message": "This is not csv file!"})
            dataset = file.read().decode('utf-8')
            io_string = io.StringIO(dataset)
            decoded_file = csv.reader(io_string, delimiter=',')
            import_from_csv(decoded_file, False, deactivate)
            cache_abstract_category_products_task.delay()
            cache_abstract_products_task.delay()
            sync_artwork_default()


        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True, "message": "Import product successfully"})
