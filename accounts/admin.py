from django.contrib import admin
from .models import User, Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'name', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['username', 'email', 'name']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'user__username']
