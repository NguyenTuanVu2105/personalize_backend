# Generated by Django 2.2.2 on 2019-11-08 03:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('notification', '0009_auto_20191108_0348'),
    ]

    operations = [
        migrations.RunSQL("alter table notification_mailhistory alter column owner_id type bigint using owner_id::bigint"),
        migrations.RunSQL("alter table notification_message alter column owner_id type bigint using owner_id::bigint"),
    ]
