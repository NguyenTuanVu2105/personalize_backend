# Generated by Django 2.2.2 on 2020-04-27 10:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0064_add_permission_admin_image_upload'),
    ]

    operations = [
        migrations.RunSQL(
            "INSERT INTO \"public\".\"auth_permission\" (\"id\", \"name\", \"content_type_id\", \"codename\") VALUES (DEFAULT, 'Admin Highlight Product View', 0, 'admin_highlight_product_view')"
            + ", (DEFAULT, 'Admin Highlight Product Update', 0, 'admin_highlight_product_update')"
        )
    ]
