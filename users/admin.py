from django.contrib import admin
from .models import AccountModel, ConfirmationCodesModel

@admin.register(AccountModel)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'country')
    search_fields = ('user__username', 'full_name', 'country')
    list_filter = ('country',)
    readonly_fields = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'country')
        }),
    )

@admin.register(ConfirmationCodesModel)
class ConfirmationCodesModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'email', 'created_at')  # Use 'email' instead of 'user'
    search_fields = ('code', 'email')  # Use 'email' instead of 'user__username'
    readonly_fields = ('code', 'email', 'created_at')  # Use 'email' instead of 'user'
    fieldsets = (
        (None, {
            'fields': ('code', 'email', 'created_at')  # Use 'email' instead of 'user'
        }),
    )
