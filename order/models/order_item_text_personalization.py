from django.db import models

from HUB.models.random_id_model import RandomIDModel


class OrderItemTextPersonalization(RandomIDModel):
    order_item = models.ForeignKey('order.OrderItem', on_delete=models.CASCADE, related_name='text_personalization_set')
    text_personalization = models.ForeignKey('user_product.TextPersonalization', on_delete=models.CASCADE)
    personal_text = models.CharField(max_length=255)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order__order_item_text_personalization"
        unique_together = ('order_item', 'text_personalization')
        ordering = ['id']

    def __str__(self):
        return "Order Item: {} | Text Personalization {}".format(self.order_item_id, self.text_personalization_id)
