from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from apps.users.models import CustomUser

admin.site.site_title = "TaxiProject Admin"
admin.site.site_header = "TaxiProject"
admin.site.index_title = "TaxiProject Admin"
admin.site.site_brand = "TaxiProject"
admin.site.welcome_sign = "TaxiProject"
admin.site.copyright = "TaxiProject"

admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['full_name']
    list_display = ['id', 'phone', 'full_name', 'role', 'is_active', 'created_at']
    list_display_links = ['phone', 'full_name', 'role']
    list_filter = ['role', 'is_active']
    fieldsets = (
        (None, {'fields': ('phone',)}),
        ('Personal info', {'fields': ('full_name', 'role')}),

        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ['phone', 'full_name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-created_at')


admin.site.register(CustomUser, CustomUserAdmin)

