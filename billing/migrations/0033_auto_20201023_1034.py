# Generated by Django 2.2.2 on 2020-10-23 09:34

from django.db import migrations, models

from billing.constants.transaction_types import TransactionType
from billing.forms.transaction import TransactionUpdateForm
from billing.models import Transaction


def migrate_payment_gateway_od(apps, schema_editor):
    for transaction in Transaction.objects.filter(payment_gateway_transaction_id="", type=TransactionType.CHARGE):
        transaction_detail = transaction.detail
        if not transaction_detail:
            continue
        transaction_form = TransactionUpdateForm(instance=transaction,
                                                 data={"detail": transaction_detail, "status": transaction.status})
        transaction_form.validate()
        transaction_form.save()


class Migration(migrations.Migration):
    dependencies = [
        ('billing', '0032_auto_20201023_0934'),
    ]

    operations = [
        migrations.RunPython(migrate_payment_gateway_od)
    ]
