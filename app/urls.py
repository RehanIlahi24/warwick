from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('cafe/', views.cafe, name='main-cafe'),
    path('cafe_detail/<int:id>/', views.cafe_detail, name='main-cafe_detail'),
    path('restaurant/', views.restaurant, name='main-restaurant'),
    path('restaurant_detail/<int:id>/', views.restaurant_detail, name='main-restaurant_detail'),
    path('team/', views.team, name='main-team'),
    path('about/', views.about, name='about'),
    path('search_bar/', views.search_bar, name='search_bar'),
]