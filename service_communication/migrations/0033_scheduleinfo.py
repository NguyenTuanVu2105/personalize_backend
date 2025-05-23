# Generated by Django 2.2.2 on 2020-07-22 08:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_communication', '0032_auto_20200716_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_type', models.CharField(choices=[('1', 'auto_scan_support_ticket')], db_index=True, default='1', max_length=10)),
                ('meta', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
            options={
                'db_table': 'service_communication_schedule_info',
            },
        ),
    ]
