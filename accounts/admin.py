from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'role', 'email', 'linked_id')
    search_fields = ('user_id', 'username', 'role', 'email')
    list_filter = ()  # 移除默认的 is_staff, is_superuser, is_active 过滤器

    fieldsets = (
        (None, {'fields': ('user_id', 'username', 'password', 'email', 'role', 'linked_id')}),
        ('Permissions', {'fields': ()}),  # 无额外数据库字段
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'username', 'password', 'email', 'role', 'linked_id')}
        ),
    )
