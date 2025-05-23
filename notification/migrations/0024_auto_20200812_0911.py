# Generated by Django 2.2.2 on 2020-08-12 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0023_auto_20200731_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instantprompt',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'add_shop'), ('1', 'add_payment_method'), ('2', 'billing_charge_failed'), ('3', 'show_tour_new_product_design'), ('4', 'show_tour_new_product_pricing'), ('5', 'show_tour_payment_manager'), ('6', 'show_shop_setting'), ('7', 'ticket_unread')], db_index=True, default='1', max_length=2),
        ),
    ]
