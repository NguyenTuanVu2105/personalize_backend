from django.db import migrations, models
from django.db.models import Q
from order.constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus
from order.constants.fulfill_statuses import OrderFulfillStatus

def update_order_deliver(apps, schema_editor):
    Order = apps.get_model("order", "Order")
    FulfillmentOrderPack = apps.get_model("order", "FulfillmentOrderPack")
    for order_obj in Order.objects.all():
        if order_obj.fulfill_status == OrderFulfillStatus.FULFILLED:
            deliver = not FulfillmentOrderPack.objects.filter(order_pack__order_id=order_obj.id).filter(
                ~Q(tracking_status=FulfilmentOrderPackTrackingStatus.DELIVERED)).exists()
            order_obj.is_delivered_order = deliver
        else:
            order_obj.is_delivered_order = False
        order_obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ('order', '0119_auto_20210407_0842'),
    ]

    operations = [
        migrations.RunPython(update_order_deliver)
    ]