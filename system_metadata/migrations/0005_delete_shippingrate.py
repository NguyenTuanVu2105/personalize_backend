# Generated by Django 2.2.2 on 2020-07-23 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0052_auto_20200723_1351'),
        ('system_metadata', '0004_auto_20191109_1112'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShippingRate',
        ),
    ]
