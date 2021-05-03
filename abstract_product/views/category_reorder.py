from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericAPIView
from abstract_product.models import AbstractProductCategory


class CategoryReorder(AdminGenericAPIView):
    error_messages = {
        "category": {
            "invalid": "This category is invalid",
        }
    }

    @method_permission_required(get_permissions(['admin_abstract_product_category_update', ]))
    def put(self, request):
        request_data = request.data
        try:
            categories = request_data['categories']
            for index, category_data in enumerate(categories):
                category = AbstractProductCategory.objects.get(id=category_data['id'])
                category.sort_index = index + 1
                category.save()
        except Exception as e:
            print(str(e))
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True, "message": "Reorder category successfully"})
