# Generated by Django 2.2.2 on 2020-12-02 09:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0050_user_is_test_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='edit_order_items_delay',
            field=models.DurationField(default=datetime.timedelta(seconds=1800), null=True),
        ),
    ]
