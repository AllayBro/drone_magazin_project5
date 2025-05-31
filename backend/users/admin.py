from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Отображаемые поля в списке пользователей
    list_display = (
        'username', 'email', 'nickname', 'role', 'is_staff', 'is_active', 'email_verified'
    )
    list_filter = ('role', 'is_staff', 'is_active', 'email_verified')

    # Поля при редактировании пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Личная информация'), {
            'fields': (
                'first_name', 'last_name', 'nickname', 'email', 'phone', 'avatar',
                'country', 'city', 'region', 'email_verified'
            )
        }),
        (_('Права доступа'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email', 'nickname')
    ordering = ('-date_joined',)
