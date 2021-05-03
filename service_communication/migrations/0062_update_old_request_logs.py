from django.contrib.contenttypes.models import ContentType
from django.db import migrations, transaction

from service_communication.constants.request_type import RequestType
from service_communication.services.service_communication_log import extract_invoice_id_from_payload


@transaction.atomic()
def update_old_paypal_request_logs(apps, schema_editor):
    ServiceCommunicationLog = apps.get_model('service_communication', 'ServiceCommunicationLog')
    Invoice = apps.get_model('billing', 'Invoice')
    updatable_request_logs = ServiceCommunicationLog.objects.exclude(payload={}).filter(
        type=RequestType.PAYMENT_PAYPAL_REQUEST).filter(object_id=None).filter(content_type_id=None)
    for request_log in updatable_request_logs:
        try:
            invoice_id = extract_invoice_id_from_payload(request_log.payload)
            invoice = Invoice.objects.get(pk=invoice_id)
            ServiceCommunicationLog.objects.filter(pk=request_log.id).update(
                content_type_id=ContentType.objects.get_for_model(Invoice).id, object_id=invoice.id)
        except Invoice.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('service_communication', '0061_auto_20210402_1228'),
    ]

    operations = [
        migrations.RunPython(update_old_paypal_request_logs),
    ]
