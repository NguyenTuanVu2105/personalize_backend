# Generated by Django 2.2.2 on 2020-12-29 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product', '0120_artworkfusion_last_fusion_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproduct',
            name='is_updated_fusions',
            field=models.BooleanField(default=False),
        ),
    ]
