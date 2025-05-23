# Generated by Django 2.2.2 on 2020-02-07 09:59

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0008_auto_20200116_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='failed_charge_count',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='next_charge_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 7, 9, 59, 9, 40276, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
