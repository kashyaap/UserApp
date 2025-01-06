from django.contrib import admin
from .models import UserDetail

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'created_at')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('created_at',)