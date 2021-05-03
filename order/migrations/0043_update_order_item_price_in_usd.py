from django.db import migrations

from system_metadata.services.currency_converter import convert_local_money_to_usd


def migrate_order_item_price_in_usd(apps, schema_editor):
    OrderItem = apps.get_model("order", "OrderItem")
    for order_item_obj in OrderItem.objects.all():
        price = order_item_obj.price
        price_in_usd = convert_local_money_to_usd(price, order_item_obj.currency)
        price_in_usd = round(price_in_usd, 5)
        previous_price_in_usd = order_item_obj.price_in_usd
        if price_in_usd != previous_price_in_usd:
            order_item_obj.price_in_usd = price_in_usd
        order_item_obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0042_auto_20200203_0628'),
    ]

    operations = [
        migrations.RunPython(migrate_order_item_price_in_usd),
    ]
