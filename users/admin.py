from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'user_type', 'is_approved', 'is_admin', 'is_deleted')
    list_filter = ('user_type', 'is_approved', 'is_admin', 'is_deleted', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('profile_pic', 'device_token', 'otp')}),
        ('Permissions', {'fields': ('user_type', 'is_admin', 'is_superuser', 'is_approved', 'is_deleted', 'is_mute', 'is_email_verified')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type', 'is_approved', 'is_admin')}
        ),
    )
