from django.contrib import admin

from .models import GeneralPaymentMethod


@admin.register(GeneralPaymentMethod)
class GeneralPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("content_object", "user_setting", "ordinal_number", "update_time")
