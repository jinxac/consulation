from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_active', 'last_name')
    search_fields = ['email']


admin.site.register(User, UserAdmin)
