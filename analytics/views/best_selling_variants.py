from rest_framework.response import Response

from HUB.viewsets.base import BaseGenericAPIView
from order.filters import OrderItemFilter
from order.models import OrderItem
from user_product.models import UserVariant
from user_product.serializers import UserVariantSerializer
from user_product.serializers.user_variant.base import UserVariantWithPreviewSerializer


class BestSellingVariantView(BaseGenericAPIView):
    def get(self, request):
        request_params = request.query_params
        queryset = OrderItem.objects.filter(order__shop__owner_id=self.request.user.pk)
        order_item_filter = OrderItemFilter(request_params, queryset=queryset)
        if not order_item_filter.is_valid():
            return Response({"errors": order_item_filter.errors})
        bounded_datetime_order_item_queryset = order_item_filter.qs

        user_variant_id_with_statistic_data = bounded_datetime_order_item_queryset.aggregate_best_selling_variants(
            limit=15)
        user_variant_id_with_statistic_dict = {item['user_variant']: item for item in
                                               user_variant_id_with_statistic_data}
        user_products = UserVariant.objects.filter(
            pk__in=user_variant_id_with_statistic_dict.keys()).prefetch_related_objects()
        user_variant_serializer = UserVariantWithPreviewSerializer(user_products, many=True)

        statistic_combined_user_variant_data = []
        for user_variant_data in user_variant_serializer.data:
            user_variant_id = user_variant_data["id"]
            statistic_values = user_variant_id_with_statistic_dict[user_variant_id]
            statistic_combined_user_variant_data.append({**statistic_values, "user_variant": user_variant_data})
        statistic_combined_user_variant_data.sort(key=lambda item: item["purchased_quantity"], reverse=True)
        return Response({"data": statistic_combined_user_variant_data})
