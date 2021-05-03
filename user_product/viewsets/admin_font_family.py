import logging
import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from user.serializers.user import BriefUserSerializer
from user_product.models import UserFontFamily
from ..filters.admin_font_filter import AdminFontFilter
from ..functions.fonts.retrieve_font_meta import retrieve_font_meta
from ..serializers import AdminFontFamilySerializer
from ..services.user_file_service import font_service

logger = logging.getLogger(__name__)

User = get_user_model()


class AdminFontFamilyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, AdminGenericViewSet):
    queryset = UserFontFamily.objects.all().order_by('title')
    serializer_class = AdminFontFamilySerializer
    filterset_class = AdminFontFilter

    def get_queryset(self):
        return self.queryset.filter(Q(owner=self.request.user.id) | Q(owner=None))

    @method_permission_required(get_permissions(['admin_font_family_view', ]))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data["users"] = BriefUserSerializer(User.objects.filter(is_staff=False), many=True).data
        return response

    @method_permission_required(get_permissions(['admin_font_family_view', ]))
    def retrieve(self, request, *args, **kwargs):
        font_instance = self.get_object()
        serializer = AdminFontFamilySerializer(instance=font_instance)
        return Response(serializer.data)

    @method_permission_required(get_permissions(['admin_font_family_add', ]))
    def create(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('font_file')
            font_title = request.POST.get('title')
            font_url, unicode_list = retrieve_font_meta(file=file, user=request.user)
            font_instance, _ = UserFontFamily.objects.update_or_create(title=font_title, font_url=font_url,
                                                                       available_characters=unicode_list)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.error(str(e))
            return Response({"success": False})
        else:
            return Response({"success": True, "data": AdminFontFamilySerializer(instance=font_instance).data})

    @method_permission_required(get_permissions(['admin_font_family_update', ]))
    def update(self, request, *args, **kwargs):
        try:
            title = request.data['title']
            font_instance = self.get_object()
            font_instance.title = title
            font_instance.save()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.error(str(e))
            return Response({"success": False})
        else:
            return Response({"success": True, "data": AdminFontFamilySerializer(instance=font_instance).data})

    @method_permission_required(get_permissions(['admin_font_family_delete', ]))
    def destroy(self, request, *args, **kwargs):
        try:
            font_instance = self.get_object()
            font_url = font_instance.font_url
            font_path = f'{settings.USER_FONT}{font_url.split(settings.USER_FONT)[-1]}'
            font_service.delete_public_file(file_path=font_path)
            font_instance.delete()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.error(str(e))
            return Response({"success": False})
        else:
            return Response({"success": True})

    @action(methods=["POST"], detail=True, url_path="activate",
            permission_classes=get_permissions(['admin_font_family_update']))
    def activate_font(self, request, *args, **kwargs):
        try:
            font_instance = self.get_object()
            font_instance.is_active = True
            font_instance.save()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.error(str(e))
            return Response({"success": False})
        else:
            return Response({"success": True})

    @action(methods=["DELETE"], detail=True, url_path="deactivate",
            permission_classes=get_permissions(['admin_font_family_update']))
    def deactivate_font(self, request, *args, **kwargs):
        try:
            font_instance = self.get_object()
            font_instance.is_active = False
            font_instance.save()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.error(str(e))
            return Response({"success": False})
        else:
            return Response({"success": True})
