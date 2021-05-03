from django.contrib import admin

from order.models import CancelShippingRequest, OrderHistory
from .models import Order, OrderPack, OrderItem, CustomerInfo
from .models.shipping_address import OrderShippingAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_id', "tags", 'note', 'fulfill_status', 'financial_status', 'customer_info', 'shop', 'create_time',
        'update_time')


@admin.register(OrderPack)
class OrderPackAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'fulfill_status')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order', 'order_pack', "item_id", "quantity", "price", "discount", "mfr_base_cost", "update_time")


@admin.register(CancelShippingRequest)
class OrderCancelShippingRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note', "admin", "admin_note", "status", "approve_time", "create_time", "update_time")


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "type", "message", "old_obj", "new_obj", "create_time")


@admin.register(CustomerInfo)
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "first_name", "last_name", "email", "phone", "create_time", "update_time")


@admin.register(OrderShippingAddress)
class OrderShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "address1", "address2", "create_time", "update_time")
