from django.contrib import admin

from .models import UserStripe


@admin.register(UserStripe)
class UserStripeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card_name', 'last4', 'exp_month', 'exp_year', 'country', 'billing_order', 'type')
