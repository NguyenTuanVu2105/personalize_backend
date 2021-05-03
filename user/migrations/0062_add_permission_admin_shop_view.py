from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0061_auto_20201217_0252'),
    ]

    operations = [
        migrations.RunSQL(
            "INSERT INTO \"public\".\"auth_permission\" (\"id\", \"name\", \"content_type_id\", \"codename\") VALUES (DEFAULT, 'Admin Shop View', 0, 'admin_shop_view')"
        )
    ]
