# Generated by Django 2.2.2 on 2020-02-20 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0044_auto_20200203_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproduct',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
