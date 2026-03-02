from django.urls import path
from . views import index, cart, update_cart, add_to_cart

urlpatterns = [
    path('', index, name = 'menu'),
    path('cart/', cart, name = 'cart'),
    path('update_cart/', update_cart, name = 'update_cart'),
    path('add_to_cart/', add_to_cart, name = 'add_to_cart'),
    
]
