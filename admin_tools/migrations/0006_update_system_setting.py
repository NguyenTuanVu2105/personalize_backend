from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('admin_tools', '0005_update_system_setting'),
    ]

    operations = [
        migrations.RunSQL(
            'INSERT INTO public.system_setting (type, name, value, create_time, update_time) VALUES '
            + "('3', 'ffm_service_setting', '{\"auto_mapping_sku\": false}', current_timestamp, current_timestamp);"
        ),
    ]
