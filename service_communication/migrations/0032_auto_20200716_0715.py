# Generated by Django 2.2.2 on 2020-07-16 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_communication', '0031_auto_20200707_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceauthenticationconfig',
            name='service_name',
            field=models.CharField(choices=[('fresh_desk_webhook', 'fresh_desk_webhook'), ('ecommerce_adapter', 'ecommerce_adapter')], max_length=20, primary_key=True, serialize=False),
        ),
    ]
