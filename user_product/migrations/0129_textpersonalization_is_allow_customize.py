# Generated by Django 2.2.2 on 2021-01-26 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product', '0128_auto_20210126_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='textpersonalization',
            name='is_allow_customize',
            field=models.BooleanField(default=True),
        ),
    ]
