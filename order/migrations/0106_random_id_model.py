from django.db import migrations

from HUB.models.random_id_model import RandomIDModel
from order.models import OrderItemTextPersonalization


def random_id_model(apps, schema_editor):
    RandomIDModel.init_random_seq(OrderItemTextPersonalization)


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0105_orderitemtextpersonalization'),
        ('user_product', '0127_random_id_model'),
    ]

    operations = [
        migrations.RunPython(random_id_model),
    ]
