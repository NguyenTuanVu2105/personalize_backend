# Generated by Django 2.2.2 on 2019-10-24 14:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0012_auto_20191024_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='code',
        ),
        migrations.RemoveField(
            model_name='userproduct',
            name='code',
        ),
    ]
