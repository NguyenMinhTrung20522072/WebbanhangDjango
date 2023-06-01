from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'), #home là hàm def (hàm def này gọi base.html)
    path('register/',views.register, name='register'),
    path('login/',views.loginPage, name='login'),
    path('search/',views.search, name='search'),
    path('logout/',views.logoutUser, name='logout'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('update_item/',views.updateItem, name='update_item'),
    path('category/',views.category, name='category'),
    path('detail/', views.detail, name='detail'),
    path('order_complete/', views.order_complete, name='order_complete'),
]