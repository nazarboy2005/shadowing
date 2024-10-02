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
    list_display = ('code', 'user', 'created_at')
    search_fields = ('code', 'user__username')
    readonly_fields = ('code', 'user', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('code', 'user', 'created_at')
        }),
    )
