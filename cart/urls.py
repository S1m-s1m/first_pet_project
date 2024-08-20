from django.urls import path

from cart.views import cart_detail, cart_add, cart_remove, cart_add_one, cart_remove_one, clear_cart

# from cart.views import Cart_View, Remove_From_Cart, Add_To_Cart, Add_One, Sub_One
#
# app_name = 'cart'
#
# urlpatterns = [
#     path('', Cart_View.as_view(), name='cart_view'),
#     path('add_to_cart/<int:pk>/', Add_To_Cart.as_view(), name='add_to_cart'),
#     path('add_one/<int:pk>/', Add_One.as_view(), name='add_one'),
#     path('sub_one/<int:pk>/', Sub_One.as_view(), name='sub_one'),
#     path('remove_from_cart/<int:pk>/', Remove_From_Cart.as_view(), name='remove_from_cart'),
# ]

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('add_one/<int:pk>/', cart_add_one, name='cart_add_one'),
    path('remove_one/<int:pk>/', cart_remove_one, name='cart_remove_one'),
    path('clear/', clear_cart, name='clear_cart'),
]