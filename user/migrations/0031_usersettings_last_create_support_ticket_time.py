# Generated by Django 2.2.2 on 2020-07-06 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_auto_20200526_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='last_create_support_ticket_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
