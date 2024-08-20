from decimal import Decimal
from django.contrib.auth import get_user_model
import pytest
from django.urls import reverse
from cart.forms import CartAddProductForm
from catalog.forms import ReviewForm, ProductForm, BrandForm, CategoryForm
from catalog.models import Product, Category, Brand, Review
from django.utils.translation import activate
from cart.context_processors import Cart

@pytest.mark.django_db
class TestCouponView:

    def test_valid_coupon(self, client_with_cart, coupon):
        url = reverse('coupon:apply')
        data = {
            'code': 'coupon_code'
        }
        response = client_with_cart.post(path=url, data=data)
        cart = Cart(client_with_cart)
        coupon.refresh_from_db()
        assert response.status_code == 302
        assert coupon.used_count == 1
        assert cart.get_total_price_after_discount() == 10

