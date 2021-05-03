from django.contrib import admin

from .models import PaypalPaymentMethod


@admin.register(PaypalPaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payer_id', 'type', 'email', 'agreement_id', 'update_time')
