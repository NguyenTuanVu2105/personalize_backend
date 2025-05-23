# Generated by Django 2.2.2 on 2020-12-30 07:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_tools', '0002_auto_20201224_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemSetting',
            fields=[
                ('type', models.CharField(choices=[('1', 'auto_send_shipping_order_notification'), ('2', 'auto_send_delivered_order_notification')], max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, null=True)),
                ('value', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'db_table': 'system_setting',
            },
        ),
    ]
