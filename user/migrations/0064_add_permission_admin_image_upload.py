from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0063_users'),
    ]

    operations = [
        migrations.RunSQL(
            "INSERT INTO \"public\".\"auth_permission\" (\"id\", \"name\", \"content_type_id\", \"codename\") VALUES (DEFAULT, 'Admin Image Upload', 0, 'admin_image_upload')"
            + ", (DEFAULT, 'Admim Image View', 0, 'admin_image_views')"
        )
    ]
