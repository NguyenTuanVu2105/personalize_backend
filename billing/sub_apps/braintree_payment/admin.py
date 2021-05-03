from django.contrib import admin

from .models import BraintreePaymentMethod


@admin.register(BraintreePaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'email', 'token', 'update_time')
