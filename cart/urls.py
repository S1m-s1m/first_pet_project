from django.urls import path

from cart.views import cart_detail, cart_add, cart_remove, cart_add_one, cart_remove_one, clear_cart

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('add_one/<int:pk>/', cart_add_one, name='cart_add_one'),
    path('remove_one/<int:pk>/', cart_remove_one, name='cart_remove_one'),
    path('clear/', clear_cart, name='clear_cart'),
]