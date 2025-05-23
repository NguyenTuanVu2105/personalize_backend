# Generated by Django 2.2.2 on 2019-10-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0004_auto_20191013_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='file_url',
            field=models.URLField(verbose_name='Artwork Url'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='thumbnail_url',
            field=models.URLField(verbose_name='Artwork Thumbnail Url'),
        ),
        migrations.AlterField(
            model_name='uservariantsidemockup',
            name='mockup_thumbnail_url',
            field=models.URLField(verbose_name='Mockup Thumbnail Url'),
        ),
        migrations.AlterField(
            model_name='uservariantsidemockup',
            name='mockup_url',
            field=models.URLField(verbose_name='Mockup Url'),
        ),
    ]
