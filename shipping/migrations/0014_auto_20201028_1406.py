# Generated by Django 2.2.2 on 2020-10-28 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0013_auto_20201002_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingstate',
            name='code',
            field=models.CharField(max_length=10),
        ),
    ]
