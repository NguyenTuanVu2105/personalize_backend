# Generated by Django 2.2 on 2020-01-09 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('service_communication', '0023_create_text_search_trigger_20200109_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecommunicationlog',
            name='webhook_job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communication_logs', to='service_communication.WebhookJob'),
        ),
    ]
