# Generated by Django 2.2 on 2020-01-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0039_artwork_create_text_search_trigger_20200114_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproduct',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
