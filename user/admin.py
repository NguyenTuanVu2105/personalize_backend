from django.contrib import admin

from .models import User, UserSettings


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'group', 'account_type', 'is_email_confirmed', 'is_valid_payment', 'phone_number', 'gender', 'address', 'birthday', 'tax_code', 'avatar')
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     (_('Personal info'), {'fields': ('name', 'address')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
    #                                    'groups', 'user_permissions')}),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2'),
    #     }),
    # )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
