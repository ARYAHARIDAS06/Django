# cart/urls.py

from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('addtocart/<int:i>', views.addtocart, name='addtocart'),
    path('addtocart/<int:i>', views.cart_decrement, name='cart_decrement'),
    path('remove/<int:i>', views.remove, name='remove'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('cart_view', views.continuee, name='continuee'),
    path('placeorder', views.placeorder, name='placeorder'),
    #path('payment_sucess', views.payment_sucess, name='payment_sucess'),


]
