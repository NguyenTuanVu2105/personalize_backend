# Generated by Django 2.2.2 on 2020-02-27 09:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0022_merge_20200222_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='next_charge_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
