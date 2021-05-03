from django.db import migrations

from billing.signals import update_order_financial_status


def migrate_orders_financial_status(apps, schema_editor):
    Invoice = apps.get_model("billing", "Invoice")
    for invoice_obj in Invoice.objects.only("id"):
        update_order_financial_status(Invoice, invoice_obj, created=False)


class Migration(migrations.Migration):
    dependencies = [
        ('billing', '0017_auto_20200210_0846'),
        ('order', '0046_order_send_support_email_time')
    ]

    operations = [
        migrations.RunPython(migrate_orders_financial_status),
    ]
