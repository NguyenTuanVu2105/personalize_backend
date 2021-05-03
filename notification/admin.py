from django.contrib import admin

from notification.models import InstantPrompt
from .models import MailHistory, Template, Message


@admin.register(MailHistory)
class MailHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MailHistory._meta.get_fields()]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Template._meta.get_fields()]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.get_fields()]


@admin.register(InstantPrompt)
class InstantPromptAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InstantPrompt._meta.get_fields()]
