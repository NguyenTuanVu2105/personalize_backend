# Generated by Django 2.2.2 on 2019-11-08 03:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('admin_tools', '0003_systemsetting'),
    ]

    operations = [
        migrations.RunSQL(
            'INSERT INTO public.system_setting (type, name, value, create_time, update_time) VALUES '
            + "('1', 'auto_send_shipping_order_notification', '{\"auto_send\": false}', current_timestamp, current_timestamp),"
            + "('2', 'auto_send_delivered_order_notification', '{\"auto_send\": true}', current_timestamp, current_timestamp);"
        ),
    ]
