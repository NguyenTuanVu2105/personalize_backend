# Generated by Django 2.2.2 on 2020-01-14 14:20
import logging

from django.db import migrations, connection

from HUB.models.random_id_model import RandomIDModel
from user_product.functions.sample_product import update_sample_product
from user_product.models import SampleProduct

logger = logging.getLogger(__name__)


def update_sample_product_execution(apps, schema_editor):
    for sample_product in SampleProduct.objects.all():
        update_sample_product(sample_product)


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0118_remove_artworkfusion_send_to_fulfill'),
    ]

    operations = [
        migrations.RunPython(update_sample_product_execution),
    ]
