# Generated by Django 2.2.2 on 2019-10-19 09:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('combine_payment', '0003_generalpaymentmethod_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalpaymentmethod',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
