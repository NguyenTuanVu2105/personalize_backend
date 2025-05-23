# Generated by Django 2.2.2 on 2020-03-06 07:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('notification', '0016_random_id_instant_prompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instantprompt',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'add_shop'), ('1', 'add_payment_method'), ('2', 'billing_charge_failed'), ('3', 'show_tour_new_product_design'), ('4', 'show_tour_new_product_pricing'), ('5', 'show_tour_payment_manager'), ('6', 'show_shop_setting')], default='1', max_length=2),
        ),
    ]
