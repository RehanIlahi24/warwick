from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('',views.login_page,name="login"),
    path('logout/',views.logout_page,name="logout"),
    path('login/', views.login_page, name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_view/', views.user_view, name='user_view'),
    path('user_detail/<str:uid>/', views.user_detail, name='user_detail'),
    path('cafe/', views.cafe, name='cafe'),
    path('cafe_detail/<int:id>/', views.cafe_detail, name='cafe_detail'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('restaurant_detail/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('dish/', views.dish, name='dish'),
    path('dish_detail/<int:id>/', views.dish_detail, name='dish_detail'),
    path('team/', views.team, name='team'),
    path('team_detail/<int:id>/', views.team_detail, name='team_detail'),
    path('reviews/', views.reviews, name='reviews'),
]
