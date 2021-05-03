import logging

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from abstract_product.constants import AbstractType
from user_product.models import UserVariant
from user_product.serializers.user_variant.base import UserVariantTYCardSerializer
from ..forms.user_settings import UserSettingsForm
from ..models import UserSettings
from ..serializers import UserSettingsSerializer

logger = logging.getLogger(__name__)


class UserSettingsViewSet(mixins.RetrieveModelMixin,
                          AuthenticatedGenericViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSettingsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSettingsSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        request_data = request.data
        user_settings = self.get_object()
        user_settings_form = UserSettingsForm(request_data, instance=user_settings)
        if user_settings_form.is_valid():
            user_settings = user_settings_form.save(commit=False)
            user_settings.request_order_processing_manually = request_data['request_order_processing_manually'] or False
            user_settings.save()
            return Response({"success": True})
        else:
            return Response({"success": False, "message": {"errors": user_settings_form.errors}})

    @action(methods=['put', 'patch'], detail=False, url_path='activate-thank-you-card')
    def set_default_thank_you_card(self, request, *args, **kwargs):
        request_data = request.data
        branding_id = request_data.get('branding')
        branding = UserVariant.objects.filter(user_product_id=branding_id).first()
        if branding.user_product.abstract_product.type == AbstractType.THANK_YOU_CARD:
            user_settings = request.user.settings
            user_settings.default_branding_card = branding
            user_settings.save()
            return Response({"success": True, 'data': self.get_serializer(user_settings).data})
        else:
            return Response({"success": False, "message": 'This product is not a branding card'})

    @action(methods=['put', 'patch'], detail=False, url_path='deactivate-thank-you-card')
    def deactivate_thank_you_card(self, request):
        user_settings = request.user.settings
        user_settings.default_branding_card = None
        user_settings.save()
        return Response({'success': True, 'data': self.get_serializer(user_settings).data})

    @action(methods=['GET'], detail=False, url_path='default-thank-you-card')
    def get_default_thank_you_card(self, request):
        user_settings = request.user.settings
        default_branding_card = user_settings.default_branding_card
        if default_branding_card:
            res_data = UserVariantTYCardSerializer(instance=default_branding_card).data
        else:
            res_data = None
        return Response({'success': True, 'data': res_data})
