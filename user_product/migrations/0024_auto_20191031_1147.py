# Generated by Django 2.2.2 on 2019-10-31 11:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user_product', '0023_update_foreign_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservariant',
            name='sku',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='SKU'),
        ),
    ]
