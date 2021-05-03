from django.contrib import admin

from .models import PaypalVaultPaymentMethod


@admin.register(PaypalVaultPaymentMethod)
class UserStripeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card_name', 'last4', 'exp_month', 'exp_year', 'type', 'payment_token')
