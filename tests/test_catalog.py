from decimal import Decimal
from django.contrib.auth import get_user_model
import pytest
from django.urls import reverse
from cart.forms import CartAddProductForm
from catalog.forms import ReviewForm, ProductForm, BrandForm, CategoryForm
from catalog.models import Product, Category, Brand, Review
from django.utils.translation import activate

pytestmark = pytest.mark.django_db

User = get_user_model()

class TestProductDetailView:

    def test_product_detail_view_get_existing_product(self, client, admin_user, products, categories):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:product_detail', kwargs={'pk': products[0].pk, 'slug': products[0].translations.get(language_code='en').slug})
        response = client.get(url)
        assert response.status_code == 200
        assert 'object' in response.context
        assert response.context['object'] == products[0]
        # assert 'cart_form' in response.context
        assert isinstance(response.context['cart_form'], CartAddProductForm)
        assert 'review_form' in response.context
        assert isinstance(response.context['review_form'], ReviewForm)
        assert 'reviews' in response.context
        assert 'category' in response.context
        assert 'recommended_products' in response.context

    def test_product_detail_view_get_nonexistent_product(self, client):
        activate('en')
        url = reverse('catalog:product_detail', kwargs={'pk': 999, 'slug': 'non-existent-product'})
        response = client.get(url)
        assert response.status_code == 200  # Assuming you render a 404 page with status 200
        assert 'error' in response.context
        assert 'There is no such product' in response.content.decode('utf-8')

    def test_product_detail_view_post_valid_review(self, client, products, admin_user):
        activate('en')
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:product_detail', kwargs={'pk': products[0].pk, 'slug': products[0].translations.get(language_code='en').slug})        
        data = {
            'text': 'This is a review.',
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        assert Review.objects.filter(product=products[0], author=admin_user).exists()
        assert Review.objects.get(product=products[0], author=admin_user).text == 'This is a review.'


    def test_product_detail_view_post_reply_to_review(self, client, products, review, admin_user):
        activate('en')
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:product_detail', kwargs={'pk': products[0].pk, 'slug': products[0].translations.get(language_code='en').slug})
        data = {
            'text': 'This is a reply.',
            'parent': review.pk
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        reply = Review.objects.filter(product=products[0], author=admin_user, parent=review).first()
        assert reply is not None
        assert reply.text == 'This is a reply.'

    def test_post_delete_review(self, client, review, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_review', kwargs={'pk': review.pk})
        response = client.post(path=url)
        assert response.status_code == 302
        # assert not Review.objects.get(pk=review.pk) #incorrect because if there is no such object it doesnt return None or etc it raise error ObjectDoesNotExists
        assert not Review.objects.filter(pk=review.pk).exists()

class TestDeleteReviewView:

    def test_get_delete_review(self, client, admin_user, review):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_review', kwargs={'pk': review.pk})
        response = client.get(path=url)
        assert response.context['object'] == review

    def test_post_delete_review(self, client, admin_user, review):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_review', kwargs={'pk': review.pk})
        response = client.post(url)
        assert response.status_code == 302
        # assert not Review.objects.get(pk=review.pk) #incorrect because if there is no such object it doesnt return None or etc it raise error ObjectDoesNotExists
        assert not Review.objects.filter(pk=review.pk).exists(), f"Review with pk={review.pk} still exists in the database"

class TestCreateProductView:

    def test_get_create_product(self, client, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:create_product')
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], ProductForm)

    def test_post_create_product(self, client, admin_user, products):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:create_product')
        data = {
            'name': 'Test product',
            'description': 'Test description',
            'category': products[0].category.pk,
            'size': products[0].size,
            'price': Decimal('20.00')
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        assert Product.objects.get(translations__language_code='en', translations__name='Test product')


class TestUpdateProductView:

    def test_update_product_view_get_existing_product(self, client, admin_user, products):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:update_product', kwargs={'pk': products[0].pk})
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], ProductForm)
        assert response.context['object'] == products[0]

    def test_update_product_view_get_nonexistent_product(self, client, admin_user, products):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:update_product', kwargs={'pk': 999})
        response = client.get(url)
        assert response.status_code == 200  # Assuming you render a 404 page with status 200
        assert 'error' in response.context
        assert 'There is no such product' in response.content.decode('utf-8')

    def test_update_product_view_post_valid_data(self, client, admin_user, products):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:update_product', kwargs={'pk': products[0].pk})
        data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'category': products[0].category.pk,
            'size': products[0].size,
            'price': Decimal('20.00')
        }

        response = client.post(url, data)
        products[0].refresh_from_db()
        assert response.status_code == 302
        assert products[0].name == 'Updated Product'
        assert products[0].price == Decimal('20.00')

class TestDeleteProductView:

    def test_get_delete_product(self, client, admin_user, products):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_product', kwargs={'pk': products[0].pk})
        response = client.get(path=url)
        assert response.context['object'] == products[0]

    def test_post_delete_product(self, client, admin_user, products):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_product', kwargs={'pk': products[0].pk})
        response = client.post(url)
        assert response.status_code == 302
        # assert not Review.objects.get(pk=review.pk) #incorrect because if there is no such object it doesnt return None or etc it raise error ObjectDoesNotExists
        assert not Product.objects.filter(pk=products[0].pk).exists(), f"Product with pk={products[0].pk} still exists in the database"

class TestBrandListView:

    def test_brand_list_view(self, client):
        url = reverse('catalog:brand_list')
        response = client.get(url)
        assert response.status_code == 200

class TestCreateBrandView:

    def test_get_create_brand(self, client, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:create_brand')
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], BrandForm)

    def test_post_create_brand(self, client, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:create_brand')
        data = {
            'name': 'Test brand',
            'description': 'Test description'
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        assert Brand.objects.get(name='Test brand')

class TestUpdateBrandView:

    def test_get_update_brand(self, client, admin_user, brands):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:update_brand', kwargs={'pk':brands[0].pk})
        response = client.get(path=url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], BrandForm)
        assert response.context['object'].name == brands[0].name

    def test_post_update_brand(self, client, admin_user, brands):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:update_brand', kwargs={'pk':brands[0].pk})
        data = {
            'name': 'New brand',
            'description': 'New description'
        }
        response = client.post(path=url, data=data)
        brands[0].refresh_from_db()
        assert response.status_code == 302
        assert brands[0].name == 'New brand'

class TestBrandDetailView:

    def test_brand_detail(self, client, brands):
        url = reverse('catalog:brand_detail', kwargs={'pk': brands[0].pk})
        response = client.get(path=url)
        assert response.context['object'] == brands[0]
        assert 'products' in response.context

class TestDeleteBrandView:

    def test_get_delete_brand(self, client, admin_user, brands):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_brand', kwargs={'pk': brands[0].pk})
        response = client.get(path=url)
        assert response.context['object'] == brands[0]

    def test_post_delete_brand(self, client, admin_user, brands):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_brand', kwargs={'pk': brands[0].pk})
        response = client.post(path=url)
        assert not Brand.objects.filter(pk=brands[0].pk).exists(), f"Brand with pk={brands[0].pk} still exists in the database"

class TestCreateCategoryView:

    def test_get_create_category(self, client, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:create_category')
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], CategoryForm)

    def test_post_create_category(self, client, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        activate('en')
        url = reverse('catalog:create_category')
        data = {
            'name': 'Test category',
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        assert Category.objects.get(translations__language_code='en', translations__name='Test category')

class TestTranslateCategoryView:

    def test_get_translate_category(self, client, admin_user, categories):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:translate_category', kwargs={'pk':categories[0].pk})
        response = client.get(path=url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], CategoryForm)
        assert response.context['object'].name == categories[0].name

    def test_post_translate_category(self, client, categories, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:translate_category', kwargs={'pk':categories[0].pk})
        data = {
            'name': 'New category',
        }
        response = client.post(path=url, data=data)
        categories[0].refresh_from_db()
        assert response.status_code == 302
        assert categories[0].name == 'New category'

class TestDeleteCategoryView:

    def test_get_delete_category(self, client, categories, admin_user):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_category', kwargs={'pk': categories[0].pk})
        response = client.get(path=url)
        assert response.context['object'] == categories[0]

    def test_post_delete_category(self, client, admin_user, categories):
        client.login(email='admin_user@gmail.com', password='admin_password')
        url = reverse('catalog:delete_category', kwargs={'pk': categories[0].pk})
        response = client.post(path=url)
        assert not Category.objects.filter(pk=categories[0].pk).exists()

