# Generated by Django 2.2.2 on 2020-02-03 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0043_update_order_item_price_in_usd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='type',
            field=models.CharField(choices=[('1', 'create_order'), ('2', 'update_order_fulfill_status'), ('3', 'update_order_financial_status'), ('4', 'update_order_shipping_address'), ('7', 'update_order_shipping_rate'), ('5', 'update_order_item_variant'), ('6', 'update_order_item_quantity'), ('8', 'update_order_is_item_editable_status')], max_length=2),
        ),
    ]
