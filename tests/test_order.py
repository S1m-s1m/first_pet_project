from decimal import Decimal
from django.contrib.auth import get_user_model
import pytest
from django.urls import reverse
from cart.forms import CartAddProductForm
from catalog.forms import ReviewForm, ProductForm, BrandForm, CategoryForm
from catalog.models import Product, Category, Brand, Review
from django.utils.translation import activate
from pet_project import settings
from order.forms import OrderForm
from cart.context_processors import Cart
from order.models import Order, Order_Item

class TestCreateOrderView:

    def test_get_create_order_view(self, client):
        url = reverse('order:create_order')
        response = client.get(path=url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], OrderForm)

    # def test_post_create_order_view(self, client_with_cart, products, coupon, user):
    #     #client_with_cart.login(email=user.email, password=user.password)
    #     url = reverse('cart:cart_add', kwargs={'pk': products[0].pk})
    #     data = {
    #         'quantity': 1,
    #         'update': False
    #     }
    #     response = client_with_cart.post(path=url, data=data)
    #     assert response.status_code == 302
    #     cart = client_with_cart.session.get(settings.CART_SESSION_ID)
    #     assert str(products[0].pk) in cart.keys()
    #     session = client_with_cart.session
    #     session['coupon_id'] == coupon.pk '''смотри вьюшку там купон в сессию добавляется через экземпляр корзины'''
    #     # session['order_pk'] == order.pk
    #     session.save()

    #     url = reverse('order:create_order')
        # data = {
        #     'user': user,
        #     'email': user.email,
        #     'address': 'home1',
        #     'city': 'Volgograd',
        #     'first_name': user.first_name,
        #     'last_name': user.last_name
        # }
    #     response = client_with_cart.post(path=url)
    #     assert response.status_code == 200
    #     assert response.context['order'] 

    # def test_create_order_view(self, client_with_cart, product, user, coupon):
    #     client = client_with_cart

    #     url = reverse('order:create_order')  # Замените на правильный URL вашей вьюшки
    #     data = {
    #         'user': user,
    #         'email': user.email,
    #         'address': 'home1',
    #         'city': 'Volgograd',
    #         'first_name': user.first_name,
    #         'last_name': user.last_name
    #     }
    #     response = client.post(url, data=data)

    #     assert response.status_code == 200
    #     assert Order.objects.count() == 1
    #     order = Order.objects.first()
    #     assert order.user == user
    #     assert order.coupon == coupon
    #     assert order.discount == coupon.discount

    #     # Проверьте, что элементы заказа были созданы
    #     assert Order_Item.objects.count() == 1
    #     order_item = Order_Item.objects.first()
    #     assert order_item.product == product
    #     assert order_item.quantity == 2

    #     # Проверьте, что корзина была очищена
    #     cart = Cart(client)
    #     assert len(cart) == 0

    #     # Проверьте, что ключ 'order_pk' установлен в сессии
    #     session = client.session
    #     assert session.get('order_pk') == order.pk


    def test_post_create_order(self, client_with_cart, user, product):
        url = reverse('order:create_order')
        data = {
            'user': user, 
            'email': user.email,
            'address': 'home1',
            'city': 'Volgograd',
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        response = client_with_cart.post(path=url, data=data)
        assert response.status_code == 200
        assert Order.objects.count() == 1
        order = Order.objects.first()
        assert order.user == user
        assert order.address == 'home1'
        assert order.city == 'Volgograd'

        assert Order_Item.objects.count() == 1
        order_item = Order_Item.objects.first()
        assert order_item.product == product
        assert order_item.order == order

        cart = Cart(client_with_cart)
        assert len(cart) == 0

class TestOrderDetailView:

    def test_order_detail_view(self, client_with_cart, user):
        url = reverse('order:create_order')
        data = {
            'user': user, 
            'email': user.email,
            'address': 'home1',
            'city': 'Volgograd',
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        response = client_with_cart.post(path=url, data=data)

        order = Order.objects.first()
        url = reverse('order:order_detail', kwargs={'pk': order.pk})
        response = client_with_cart.get(path=url)

        assert response.status_code == 200
        assert response.context['object'] == order

class TestAdminOrderDetailView:

    def test_admin_order_detail_view(self, admin_client_with_cart, admin_user):
        url = reverse('order:create_order')
        data = {
            'user': admin_user, 
            'email': admin_user.email,
            'address': 'home1',
            'city': 'Volgograd',
            'first_name': admin_user.first_name,
            'last_name': admin_user.last_name
        }
        response = admin_client_with_cart.post(path=url, data=data)

        order = Order.objects.first()
        url = reverse('order:order_detail', kwargs={'pk': order.pk})
        response = admin_client_with_cart.get(path=url)

        assert response.status_code == 200
        assert response.context['object'] == order

class TestAdminOrderPDF:
    def test_admin_order_pdf(self, admin_client_with_cart, admin_user):
        admin_client_with_cart.login(username=admin_user.email, password=admin_user.password)
        url = reverse('order:create_order')
        data = {
            'user': admin_user, 
            'email': admin_user.email,
            'address': 'home1',
            'city': 'Volgograd',
            'first_name': admin_user.first_name,
            'last_name': admin_user.last_name
        }
        response = admin_client_with_cart.post(path=url, data=data)
        assert Order_Item.objects.count() == 1
        order = Order.objects.first()

        url = reverse('order:admin_order_pdf', kwargs={'pk': order.pk})
        response = admin_client_with_cart.get(path=url)
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
        assert 'Content-Disposition' in response
        assert f'filename=order_{order.pk}.pdf' in response['Content-Disposition']


