# Generated by Django 2.2.2 on 2020-10-02 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abstract_product', '0045_abstractproductmeta_template_meta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractproductvariant',
            name='additional_cost',
        ),
        migrations.RemoveField(
            model_name='abstractproductvariant',
            name='base_cost',
        ),
        migrations.RemoveField(
            model_name='abstractproductvariant',
            name='fulfill_additional_cost',
        ),
        migrations.RemoveField(
            model_name='abstractproductvariant',
            name='fulfill_base_cost',
        ),
    ]
