from django.contrib import admin

from billing.models import Invoice, InvoicePack, InvoiceItem, Transaction, Refund


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'create_time', 'update_time', 'paid_time')


@admin.register(InvoicePack)
class InvoicePackAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'invoice', 'order_pack', 'production_cost', 'shipping_cost', 'tax', 'currency', 'create_time', 'update_time')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'invoice_pack', 'order_item', 'quantity', 'price', 'currency', 'create_time', 'update_time')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "content_object", "payment_gateway", "payment_method", "type", "amount", "status", "create_time")


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
        "id", "content_object", "user", "invoice", "refund_type", "description", "amount", "currency", "status",
        "create_time", "update_time")
