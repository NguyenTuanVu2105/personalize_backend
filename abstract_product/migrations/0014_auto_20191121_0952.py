# Generated by Django 2.2.2 on 2019-11-21 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('abstract_product', '0013_auto_20191121_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractvariantsidemockupinfo',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='abstractvariantsidemockupinfo',
            name='update_time',
        ),
        migrations.AlterField(
            model_name='abstractvariantsidemockupinfo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
