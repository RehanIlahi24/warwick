from django.contrib import admin
from .models import User
# Register your models here.


class adminuser(admin.ModelAdmin):
    list_display = ['uid', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active']
    search_fields = ['email','first_name','last_name','username']
admin.site.register(User, adminuser)
