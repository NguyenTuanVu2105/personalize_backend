# Generated by Django 2.2.2 on 2020-10-12 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_communication', '0040_auto_20201012_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhookjob',
            name='queue_id',
            field=models.CharField(choices=[('1', 'task_run_webhook_job_fulfillment_order'), ('2', 'task_run_webhook_job_fulfillment_product'), ('3', 'task_run_webhook_job_adapter_order'), ('4', 'task_run_webhook_job_adapter_product'), ('5', 'task_run_webhook_job_ex_adapter_shop_user_product_from_others'), ('6', 'task_run_webhook_job_mockup_artwork_fusion'), ('7', 'task_run_webhook_job_adapter_app')], db_index=True, max_length=2),
        ),
    ]
