# Generated by Django 2.2.2 on 2021-03-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0111_auto_20210310_0356'),
    ]

    operations = [
        migrations.RunSQL("UPDATE public.order SET seller_edit_time = create_time WHERE true")
    ]
