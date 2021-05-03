from django.core.exceptions import ValidationError
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from coupon.filters.coupon_filters import CouponFilter
from coupon.models import Coupon
from coupon.serializers.admin import AdminCouponSerializer, AdminBriefCouponSerializer
from coupon.services.coupon import update_or_create_coupon


class AdminCouponViewSet(SearchableListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         AdminGenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = AdminCouponSerializer
    filterset_class = CouponFilter

    @method_permission_required(get_permissions(['admin_coupon_view', ]))
    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminBriefCouponSerializer
        return super().list(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_coupon_view', ]))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_coupon_view', ]))
    def create(self, request, *args, **kwargs):
        try:
            coupon_obj = update_or_create_coupon(request.data)
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True, "coupon": self.serializer_class(coupon_obj).data})

    @method_permission_required(get_permissions(['admin_coupon_view', ]))
    def update(self, request, *args, **kwargs):
        try:
            coupon_obj = update_or_create_coupon(request.data, existing_coupon_obj=self.get_object())
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True, "coupon": self.serializer_class(coupon_obj).data})
