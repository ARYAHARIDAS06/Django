from django.urls import path
from . import views
app_name = "shop"

urlpatterns = [
    path('',views.index,name='index'),
    path('',views.categories,name='categories'),
    path('products/<int:i>',views.products,name='products'),
    path('product_details/<int:i>',views.product_details,name='product_details'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout')
    ]