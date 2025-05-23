# Generated by Django 2.2.2 on 2020-08-06 10:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service_communication', '0033_scheduleinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhookjob',
            name='next_run_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='webhookjob',
            name='queue_id',
            field=models.CharField(choices=[('1', 'task_run_webhook_job_fulfillment_order'), ('2', 'task_run_webhook_job_fulfillment_product'), ('3', 'task_run_webhook_job_adapter_order'), ('4', 'task_run_webhook_job_adapter_product'), ('5', 'task_run_webhook_job_ex_adapter_shop_user_product_from_others')], db_index=True, default=1, max_length=2),
            preserve_default=False,
        ),
    ]
