from django.urls import path
from . views import index, cart

urlpatterns = [
    path('', index, name = 'menu'),
    path('/cart', cart, name = 'cart'),
    
]
