from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from allauth.account.models import EmailAddress

from .models import User, Profile

# ------------------------------------------------------
# USER ADMIN
# ------------------------------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'handle', 'role', 'is_active', 'is_staff', 'is_email_verified', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'email_verified', 'created_at')
    search_fields = ['username', 'email', 'handle', 'first_name', 'last_name']
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('handle', 'first_name', 'last_name', 'role', 'preferred_language')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at', 'last_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    def is_email_verified(self, obj):
        return EmailAddress.objects.filter(user=obj, verified=True, primary=True).exists()

    is_email_verified.boolean = True
    is_email_verified.short_description = 'Email Verified'


# ------------------------------------------------------
# PROFILE ADMIN
# ------------------------------------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'occupation', 'joined_date')
    list_filter = ('joined_date', 'updated_at')
    search_fields = ['user__username', 'user__email', 'full_name', 'phone_number', 'occupation']
    readonly_fields = ('joined_date', 'updated_at')
    raw_id_fields = ('user',)
    date_hierarchy = 'joined_date'


# ------------------------------------------------------
# REGISTER MODELS
# ------------------------------------------------------
# Models are registered using decorators above
