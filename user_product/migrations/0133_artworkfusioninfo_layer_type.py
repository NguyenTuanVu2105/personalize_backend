# Generated by Django 2.2.2 on 2021-03-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product', '0132_merge_20210323_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='artworkfusioninfo',
            name='layer_type',
            field=models.CharField(choices=[('1', 'artwork'), ('2', 'text_personalization')], default='1', max_length=50),
            preserve_default=False,
        ),
    ]
