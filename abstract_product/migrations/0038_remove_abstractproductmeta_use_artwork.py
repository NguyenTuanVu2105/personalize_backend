# Generated by Django 2.2.2 on 2020-07-22 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abstract_product', '0037_abstractproductmeta_use_artwork'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractproductmeta',
            name='use_artwork',
        ),
    ]
