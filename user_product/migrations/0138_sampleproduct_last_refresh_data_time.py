# Generated by Django 2.2.2 on 2021-03-31 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product', '0137_userfontfamily_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleproduct',
            name='last_refresh_data_time',
            field=models.DateTimeField(null=True),
        ),
    ]
