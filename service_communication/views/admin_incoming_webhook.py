from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from service_communication.constants.incoming_webhook_statuses import INCOMING_WEBHOOK_STATUS_CHOICES
from service_communication.constants.incoming_webhook_types import INCOMING_WEBHOOK_TYPE_CHOICES
from service_communication.models import IncomingWebhook
from service_communication.serializers.incoming_webhook import IncomingWebhookSerializer
from service_communication.services.incoming_webhook import cancel_incoming_webhook, process_incoming_webhook


class AdminIncomingWebhookViewSet(SearchableListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  AdminGenericViewSet):
    queryset = IncomingWebhook.objects.all()
    serializer_class = IncomingWebhookSerializer
    filterset_fields = ('type', 'status')

    def get_queryset(self):
        return self.queryset.prefetch_related("relate_object")

    def get_options(self):
        return {
            'status': INCOMING_WEBHOOK_STATUS_CHOICES,
            'type': INCOMING_WEBHOOK_TYPE_CHOICES
        }

    @method_permission_required(get_permissions(['admin_order_view', ]))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['options'] = self.get_options()
        return response

    @action(methods=["POST"], detail=True, url_path="cancel")
    def cancel(self, request, *args, **kwargs):
        return self.handle_request(request, cancel_incoming_webhook)

    @action(methods=["POST"], detail=True, url_path="process")
    def process(self, request, *args, **kwargs):
        return self.handle_request(request, AdminIncomingWebhookViewSet.process_webhook)

    @staticmethod
    def process_webhook(request, rejected_request, request_data):
        process_incoming_webhook(rejected_request)

    def handle_request(self, request, handle_request):
        request_data = request.data
        incoming_webhook = self.get_object()
        handle_request(request.user, incoming_webhook, request_data)
        return Response({"success": True})
