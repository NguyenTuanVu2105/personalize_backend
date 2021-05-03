import json
import logging

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.helpers.error_messages import to_standard_error_messages
from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from notification.form.notification_template_update_form import NotificationTemplateUpdateForm
from notification.models import Template
from notification.serializers.template import TemplateSerializer
from notification.services.notification import send_user_email

logger = logging.getLogger(__name__)


class NotificationTemplateViewSet(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  AdminGenericViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    lookup_field = 'type'
    error_messages = {
        **to_standard_error_messages(Template.ATTRIBUTE_LABELS)
    }

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_notification_template_view', ]))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_notification_template_view', ]))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @action(methods=['POST'], detail=True, url_path="send-sample",
            permission_classes=get_permissions(['admin_notification_template_view']))
    def send_sample_email(self, request, *args, **kwargs):
        data = request.data
        send_html = data.get('send_html') or False
        email = data.get('receiver')
        params = json.loads(data.get('param') or '{}')
        send_user_email(request.user, self.get_object(), params, email_list=[email], send_html=send_html)
        return Response({'success': True, 'message': 'Send email successful'})

    @method_permission_required(get_permissions(['admin_notification_template_update', ]))
    def update(self, request, *args, **kwargs):
        request_data = request.data
        user_product_update_form = NotificationTemplateUpdateForm(data=request_data, instance=self.get_object())
        user_product_update_form.validate()
        template = user_product_update_form.save()
        return Response({"success": True, "data": TemplateSerializer(instance=template).data})
