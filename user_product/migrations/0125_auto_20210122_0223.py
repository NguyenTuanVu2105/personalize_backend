# Generated by Django 2.2.2 on 2021-01-22 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product', '0124_auto_20210121_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artworkfusioninfo',
            name='is_visible',
        ),
        migrations.AddField(
            model_name='artworkfusioninfo',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
