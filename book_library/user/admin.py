from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdminArea(admin.ModelAdmin):
    list_display = ['is_active', 'first_name', 'last_name']
    list_display_links = ['first_name', 'last_name']
    list_editable = ['is_active']
    search_fields = ['first_name', 'last_name']
    list_filter = ['is_active']
    list_per_page = 10