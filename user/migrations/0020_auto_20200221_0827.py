# Generated by Django 2.2.2 on 2020-02-21 08:27

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0019_auto_20200221_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='next_charge_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 21, 8, 27, 14, 143843, tzinfo=utc)),
        ),
    ]
