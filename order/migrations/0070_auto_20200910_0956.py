# Generated by Django 2.2.2 on 2020-09-10 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0069_auto_20200908_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinvalid',
            name='order',
        ),
        migrations.AddField(
            model_name='orderinvalid',
            name='order_id',
            field=models.CharField(default='1', max_length=20),
        ),
        migrations.AddField(
            model_name='orderinvalid',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='type',
            field=models.CharField(choices=[('1', 'create_order'), ('2', 'update_order_fulfill_status'), ('3', 'update_order_financial_status'), ('4', 'update_order_shipping_address'), ('7', 'update_order_shipping_rate'), ('5', 'update_order_item_variant'), ('6', 'update_order_item_quantity'), ('8', 'update_order_is_item_editable_status'), ('9', 'create_support_ticket'), ('10', 'update_support_ticket'), ('11', 'reject_item_by_fulfill'), ('12', 'reject_not_support_shipping_item'), ('13', 'reject_no_shipping_item')], max_length=2),
        ),
        migrations.AlterField(
            model_name='orderinvalid',
            name='reason_code',
            field=models.CharField(blank=True, choices=[('1', 'no_customer_info'), ('2', 'no_shipping_address'), ('3', 'not_support_shipping'), ('4', 'fulfill_rejected'), ('5', 'item_not_in_printholo'), ('6', 'shop_invalid'), ('7', 'other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='orderinvalid',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invalid_order', to='shop.Shop'),
        ),
    ]
