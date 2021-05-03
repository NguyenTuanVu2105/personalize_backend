from django.contrib import admin

from shop.models import OrderScanInfo, ShopShippingRateMapping
from .models import Ecommerce, Shop


@admin.register(Ecommerce)
class EcommerceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'currency', 'ecommerce', 'create_time', 'update_time', 'status')


@admin.register(OrderScanInfo)
class OrderScanInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'update_time', 'last_order_update_time', 'checked_order_ids')


@admin.register(ShopShippingRateMapping)
class ShopShippingRateMappingAdmin(admin.ModelAdmin):
    list_display = ('shop', 'e_commerce_shipping_rate_name', 'shipping_rate', 'create_time', 'update_time')
