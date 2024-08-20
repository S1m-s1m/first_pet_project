from django.urls import path, re_path
from order.views import Create_Order, Order_Detail, Order_History, admin_order_detail, admin_order_pdf

app_name = 'order'

urlpatterns = [
    path('', Create_Order.as_view(), name='create_order'),
    path('order_history/', Order_History.as_view(), name='order_history'),
    path('order_detail/<int:pk>/', Order_Detail.as_view(), name='order_detail'),
    path('admin/<int:pk>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:pk>/pdf/', admin_order_pdf, name='admin_order_pdf'),
]