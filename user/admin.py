from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role')


admin.site.register(CustomUser, CustomUserAdmin)
