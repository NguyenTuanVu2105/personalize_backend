from django.contrib import admin

from billing.sub_apps.payoneer_payment.models.user_payoneer_payment_method import UserPayoneerPaymentMethod


@admin.register(UserPayoneerPaymentMethod)
class UserPayoneerPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payee_id')
