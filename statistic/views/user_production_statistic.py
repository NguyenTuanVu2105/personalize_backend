from django.db.models import Count
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericAPIView
from user_product.constants import UserProductStatus
from user_product.models import UserProduct


class UserProductStatisticView(AdminGenericAPIView):
    def get(self, request):
        queryset = UserProduct.objects.select_related('user', 'abstract_product') \
            .filter(status=UserProductStatus.ACTIVE) \
            .values('user', 'user__email', 'user__name', 'user__create_time', 'abstract_product',
                    'abstract_product__title') \
            .annotate(count=Count('id')).order_by('user__create_time')
        data = {}
        for record in queryset:
            if record['user'] not in data:
                data[record['user']] = {
                    'name': record['user__name'],
                    'email': record['user__email'],
                    'user create time': record['user__create_time'],
                    'products': []
                }
            data[record['user']]['products'].append({
                'id': record['abstract_product'],
                'title': record['abstract_product__title'],
                'count': record['count']
            })
        return Response(data)
