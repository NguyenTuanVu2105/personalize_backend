from django.core.exceptions import ValidationError
from rest_framework import mixins
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from coupon.models import CouponCampaign
from coupon.serializers.admin import AdminCouponCampaignSerializer
from coupon.services.coupon_campaign import update_or_create_coupon_campaign


class AdminCouponCampaignViewSet(SearchableListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 AdminGenericViewSet):
    queryset = CouponCampaign.objects.all()
    serializer_class = AdminCouponCampaignSerializer

    @method_permission_required(get_permissions(['admin_coupon_campaign_view', ]))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_coupon_campaign_view', ]))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_coupon_campaign_view', ]))
    def create(self, request, *args, **kwargs):
        try:
            coupon_campaign_obj = update_or_create_coupon_campaign(request.data)
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True, "coupon": self.serializer_class(coupon_campaign_obj).data})

    @method_permission_required(get_permissions(['admin_coupon_campaign_view', ]))
    def update(self, request, *args, **kwargs):
        try:
            coupon_campaign_obj = update_or_create_coupon_campaign(request.data,
                                                                   existing_coupon_campaign_obj=self.get_object())
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True, "coupon": self.serializer_class(coupon_campaign_obj).data})
