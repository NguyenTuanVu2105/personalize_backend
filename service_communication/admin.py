from django.contrib import admin

from service_communication.models import ServiceCommunicationLog, WebhookJob


@admin.register(ServiceCommunicationLog)
class ServiceCommunicationLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'webhook_job', 'type', 'relate_object', 'status_code', 'response_body', 'request_time', 'response_time')


@admin.register(WebhookJob)
class WebhookJobAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'request_type', 'relate_object', 'status', 'is_aborted', 'attempted_count', 'max_attempt_count',
        'create_time', 'update_time')
