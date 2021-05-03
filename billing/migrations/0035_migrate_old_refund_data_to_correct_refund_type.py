from django.db import migrations

from billing.constants.refund_types import RefundType
from billing.signals import update_order_financial_status


def migrate_old_refund_data_to_correct_refund_type(apps, schema_editor):
    Refund = apps.get_model("billing", "Refund")
    Refund.objects.filter(description__contains="Rejected Order Item IDs:").update(
        refund_type=RefundType.REJECT_ORDER_ITEMS)


class Migration(migrations.Migration):
    dependencies = [
        ('billing', '0034_invoicepack_discount'),
    ]

    operations = [
        migrations.RunPython(migrate_old_refund_data_to_correct_refund_type),
    ]
