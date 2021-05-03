from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.db import migrations

from billing.sub_apps.combine_payment.models import GeneralPaymentMethod


def remove_all_old_paypal_payment_methods(*args, **kwargs):
    paypal_method_content_type = ContentType.objects.filter(app_label="paypal_payment", model="paymentmethod").first()
    if paypal_method_content_type:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM {} WHERE content_type_id = {}'''.format(GeneralPaymentMethod._meta.db_table,
                                                                                  paypal_method_content_type.pk))


class Migration(migrations.Migration):
    dependencies = [
        ('combine_payment', '0005_auto_20191026_1548'),
    ]

    operations = [
        migrations.RunPython(remove_all_old_paypal_payment_methods)
    ]
