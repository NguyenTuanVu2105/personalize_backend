from django.contrib import admin

from worker_payment_processor.models import InvoiceProcessInfo


@admin.register(InvoiceProcessInfo)
class InvoiceProcessInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice')
