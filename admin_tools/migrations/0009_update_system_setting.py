from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('admin_tools', '0008_auto_20210308_0309'),
    ]

    operations = [
        migrations.RunSQL(
            'INSERT INTO public.system_setting (type, name, value, create_time, update_time) VALUES '
            + "('4', 'auto_send_unprofitable_order_notification', '{\"auto_send\": false}', current_timestamp, current_timestamp);"
        ),
    ]
