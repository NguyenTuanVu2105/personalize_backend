# Generated by Django 2.2.2 on 2021-02-18 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0104_fulfillmentorderpack_origin_tracking_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulfillmentorderpack',
            name='manually_update',
            field=models.BooleanField(default=False),
        ),
    ]
