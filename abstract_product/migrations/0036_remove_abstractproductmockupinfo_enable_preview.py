# Generated by Django 2.2.2 on 2020-05-05 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abstract_product', '0035_auto_20200505_0414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractproductmockupinfo',
            name='enable_preview',
        ),
    ]
