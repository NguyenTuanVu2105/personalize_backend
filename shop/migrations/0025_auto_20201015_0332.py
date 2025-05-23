# Generated by Django 2.2.2 on 2020-10-15 03:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20201014_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='confirm_installation_params',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('0', 'inactive'), ('1', 'active'), ('2', 'error'), ('3', 'unauth')], db_index=True, default='1', max_length=2),
        ),
    ]
