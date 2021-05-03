import traceback

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from service_communication.models import WebhookJob
from service_communication.serializers import WebhookJobSerializer, BriefWebhookJobSerializer
from service_communication.services import WebhookJobService
from service_communication.services.webhook_job_services import WebhookJobRecoveryService


class WebhookJobViewSet(SearchableListModelMixin,
                        mixins.RetrieveModelMixin,
                        AdminGenericViewSet):
    queryset = WebhookJob.objects.all()
    serializer_class = WebhookJobSerializer
    filterset_fields = ('request_type', 'status')

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_webhook_job_view', ]))
    def list(self, request, *args, **kwargs):
        self.serializer_class = BriefWebhookJobSerializer
        return super().list(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_webhook_job_view', ]))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @action(methods=["POST"], detail=True, url_path="recover",
            permission_classes=get_permissions(['admin_webhook_job_update', ]))
    def recover_webhook_job(self, request, pk, *args, **kwargs):
        response = self.run_webhook_job_with_function(pk, WebhookJobRecoveryService.recover_job)
        return response

    @action(methods=["POST"], detail=True, url_path="cancel",
            permission_classes=get_permissions(['admin_webhook_job_update', ]))
    def cancel_webhook_job(self, request, pk, *args, **kwargs):
        response = self.run_webhook_job_with_function(pk, WebhookJobService.stop_job)
        return response

    def run_webhook_job_with_function(self, pk, function):
        success = False
        try:
            function(pk)
        except (AssertionError) as e:
            pass
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        else:
            success = True
        return Response({"success": success})
