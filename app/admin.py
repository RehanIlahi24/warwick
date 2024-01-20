from django.contrib import admin
from .models import CafeResturant, Reviews, Team, Dish

class AdminCafeResturant(admin.ModelAdmin):
    list_display = ['id', 'cafe_name', 'image', 'type_of', 'location', 'description', 'contact_number', 'opening_time', 'closing_time', 'created_at', 'updated_at']
    list_filter = ['type_of']
    search_fields = ['cafe_name','location','contact_number']
admin.site.register(CafeResturant, AdminCafeResturant)

class admindish(admin.ModelAdmin):
    list_display = ['id', 'cafe', 'dish_name', 'ingredients', 'meal_name', 'image', 'price', 'created_at', 'updated_at']
    list_filter = ['cafe', 'meal_name']
    search_fields = ['dish_name']
admin.site.register(Dish, admindish)

class adminteam(admin.ModelAdmin):
    list_display = ['id', 'cafe', 'name', 'image', 'post', 'description', 'created_at', 'updated_at']
    list_filter = ['cafe', 'post']
    search_fields = ['name','post']
admin.site.register(Team, adminteam)

class adminrevies(admin.ModelAdmin):
    list_display = ['id', 'cafe', 'rating', 'comment', 'created_at']
    list_filter = ['rating','cafe']
admin.site.register(Reviews, adminrevies)