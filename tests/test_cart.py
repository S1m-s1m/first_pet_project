from django.urls import reverse
from pet_project import settings
from coupon.forms import CouponApplyForm
from cart.context_processors import Cart
from catalog.models import Product
from order.models import Order, Order_Item
import pytest

pytestmark = pytest.mark.django_db

class TestCartAddView:

    def test_cart_add_view(self, client, product):
        session = client.session
        session[settings.CART_SESSION_ID] = {}
        session.save()
        url = reverse('cart:cart_add', kwargs={'pk': product.pk})
        data = {
            'quantity': 1,
            'update': False
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        cart = client.session.get(settings.CART_SESSION_ID)
        assert str(product.pk) in cart.keys()

class TestCartRemoveView:

    def test_cart_remove_view(self, client_with_cart, product):
        url = reverse('cart:cart_remove', kwargs={'pk': product.pk})
        response = client_with_cart.get(path=url)
        assert response.status_code == 302
        cart = client_with_cart.session.get(settings.CART_SESSION_ID)
        assert str(product.pk) not in cart.keys()

class TestCartDetail:

    def test_cart_detail_view(self, client_with_recommendations, user):
        products = Product.objects.all()
        url = reverse('order:create_order')
        data = {
            'user': user, 
            'email': user.email,
            'address': 'home1',
            'city': 'Volgograd',
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        response = client_with_recommendations.post(path=url, data=data)
        assert response.status_code == 200
        assert Order.objects.count() == 1
        order = Order.objects.first()
        assert order.user == user
        assert order.address == 'home1'
        assert order.city == 'Volgograd'

        assert Order_Item.objects.count() == 3
        order_item = Order_Item.objects.first()
        assert order_item.product == products[0]
        assert order_item.order == order

        cart = Cart(client_with_recommendations)
        assert len(cart) == 0
        cart.add(product=products[0])
        session = client_with_recommendations.session
        session[settings.CART_SESSION_ID] = cart.cart
        session.save()
        url = reverse('cart:cart_detail')
        response = client_with_recommendations.get(path=url)
        print(response.context)
        assert response.status_code == 200
        assert isinstance(response.context['coupon_apply_form'], CouponApplyForm)
        assert response.context['recommended_products'] == [products[1], products[2]]

class TestCartAddOneView:

    def test_cart_add_one_view(self, client_with_cart, product):
        # product = Product.objects.get(pk=1)
        # url = reverse('cart:cart_add', kwargs={'pk': product.pk})
        # data = {
        #     'quantity': 1,
        #     'update': False
        # }
        # response = client_with_cart.post(path=url, data=data)
        # assert response.status_code == 302
        url = reverse('cart:cart_add_one', kwargs={'pk': product.pk})
        response = client_with_cart.get(path=url)
        cart = client_with_cart.session.get(settings.CART_SESSION_ID)
        assert response.status_code == 302
        assert cart[str(product.pk)]['quantity'] == 3

class TestCartRemoveOneView:

    def test_cart_remove_one_view(self, client_with_cart, product):
        # product = Product.objects.get(pk=1)
        # url = reverse('cart:cart_add', kwargs={'pk': product.pk})
        # data = {
        #     'quantity': 2,
        #     'update': False
        # }
        # response = client_with_cart.post(path=url, data=data)
        # assert response.status_code == 302
        url = reverse('cart:cart_remove_one', kwargs={'pk': product.pk})
        response = client_with_cart.get(path=url)
        cart = client_with_cart.session.get(settings.CART_SESSION_ID)
        assert response.status_code == 302
        assert cart[str(product.pk)]['quantity'] == 1

class TestClearCartView:

    def test_clear_cart_view(self, client_with_cart, product):
        # product = Product.objects.get(pk=1)
        # url = reverse('cart:cart_add', kwargs={'pk': product.pk})
        # data = {
        #     'quantity': 1,
        #     'update': False
        # }
        # response = client_with_cart.post(path=url, data=data)
        # assert response.status_code == 302
        url = reverse('cart:clear_cart')
        response = client_with_cart.get(path=url)
        cart = client_with_cart.session.get(settings.CART_SESSION_ID)
        assert response.status_code == 302
        assert cart == None



