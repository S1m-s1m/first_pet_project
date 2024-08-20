from decimal import Decimal
import factory
from django.contrib.auth import get_user_model
import pytest
from factory.django import DjangoModelFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image
import io
from catalog.models import Product, Category, Brand, Review
from coupon.models import Coupon
from order.models import Order, Order_Item
from pet_project import settings
from django.utils import timezone
from cart.context_processors import Cart

pytestmark = pytest.mark.django_db

User = get_user_model()

def generate_fake_image():
    fake = Faker()
    color = fake.color_name()#generate random color
    image = Image.new('RGB', (100, 100), color=color)#create image
    buffer = io.BytesIO()#save image in byte stream
    image.save(buffer, 'PNG')#save in formt png
    buffer.seek(0)#return pointer in start of the stream in order to it was able to read
    return buffer

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    @factory.post_generation#method that would be called after object of this class had been created
    def create_translations(self, create, extracted, **kwargs):
        if create:
            self.create_translation('ru', name=f'Категория {self.id}', slug=f'kategoriya-{self.id}')
            self.create_translation('en', name=f'Category {self.id}', slug=f'category-{self.id}')

class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    slug = factory.Sequence(lambda n: f'brand-{int(n)+1}')
    name = factory.Sequence(lambda n: f'Brand {int(n)+1}')
    image = factory.LazyAttribute(lambda x: SimpleUploadedFile('random_image.png', generate_fake_image().read(), content_type='image/png'))

    @factory.post_generation
    def create_translations(self, create, extracted, **kwargs):
        if create:
            self.create_translation('ru', description=f'описание{self.id}')
            self.create_translation('en', description=f'description{self.id}')

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    availability = True
    price = Decimal('10.00')
    image = factory.LazyAttribute(lambda x: SimpleUploadedFile('random_image.png', generate_fake_image().read(), content_type='image/png'))

    @factory.post_generation
    def create_translations(self, create, extracted, **kwargs):
        if create:
            self.create_translation('ru', name=f'Товар {self.id}', slug=f'tovar-{self.id}')
            self.create_translation('en', name=f'Product {self.id}', slug=f'product-{self.id}')

@pytest.fixture
def categories(db):
    return CategoryFactory.create_batch(3) # Create 3 categories

@pytest.fixture
def brands(db):
    return BrandFactory.create_batch(3)  # Create 3 brands

@pytest.fixture(scope='function')
def products(db, categories, brands):
    products = []
    for i in range(3):
        print(i)
        product = ProductFactory(category=categories[i], brand=brands[i])
        products.append(product)
    return products

# @pytest.fixture(autouse=True)
# def clear_database(transactional_db):
#     call_command('flush', '--noinput')
#     yield
#     call_command('flush', '--noinput')

# @pytest.fixture
# def categories(transactional_db):
#     category1 = CategoryFactory.create(id=1)
#     category2 = CategoryFactory.create(id=2)
#     category3 = CategoryFactory.create(id=3)
#     return [category1, category2, category3]

# @pytest.fixture
# def brands(transactional_db):
#     brand1 = BrandFactory.create(id=1)
#     brand2 = BrandFactory.create(id=2)
#     brand3 = BrandFactory.create(id=3)
#     return [brand1, brand2, brand3]

# @pytest.fixture
# def products(transactional_db, categories, brands):
#     product1 = ProductFactory.create(id=1, category=categories[0], brand=brands[0])
#     product2 = ProductFactory.create(id=2, category=categories[1], brand=brands[1])
#     product3 = ProductFactory.create(id=3, category=categories[2], brand=brands[2])
#     return [product1, product2, product3]

# @pytest.fixture
# def categories(transactional_db):
#     return CategoryFactory.create_batch(3) # Create 3 categories

# @pytest.fixture
# def brands(transactional_db):
#     return BrandFactory.create_batch(3)  # Create 3 brands

# @pytest.fixture
# def products(transactional_db, categories, brands):
#     products = []
#     for i in range(3):
#         print(i)
#         product = ProductFactory(category=categories[i], brand=brands[i])
#         products.append(product)
#     return products
    

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password', email='user@gmail.com', first_name='first_name', last_name='last_name', is_superuser=False ,is_staff=False, is_active=True)

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username='adminuser', password='admin_password', email='admin_user@gmail.com', first_name='first_name', last_name='last_name', is_superuser=True, is_staff=True,  is_active=True)

@pytest.fixture
def category(db):
    category = Category.objects.create()
    category.create_translation('ru', name='Категория 1', slug='kategoriya-1')
    category.create_translation('en', name='Category 1', slug='category-1')
    return category

@pytest.fixture
def brand(db):
    image = SimpleUploadedFile('test_image.png', generate_fake_image().read(), content_type='image/png')
    brand = Brand.objects.create(slug='brand-1', name='Brand 1', image=image)
    brand.create_translation('ru', description='описание1')
    brand.create_translation('en', description='description1')
    return brand

@pytest.fixture
def product(db, category, brand):
    image = SimpleUploadedFile('test_image.png', generate_fake_image().read(), content_type='image/png')
    product = Product.objects.create(category=category, brand=brand, availability=True, price=10, image=image)
    product.create_translation('ru', name='Товар 1', slug='tovar-1')
    product.create_translation('en', name='Product 1', slug='product-1')
    return product

@pytest.fixture
def review(db, products, user):
    review = Review.objects.create(product=products[0], author=user, text='test comment')
    return review

@pytest.fixture
def coupon(db):
    coupon = Coupon.objects.create(code='coupon_code', valid_from=timezone.now(), valid_to=timezone.datetime(2024, 9, 1, 0, 0), discount=50, active=True)
    return coupon

@pytest.fixture
def client_with_cart(db, client, product, coupon, user):
    client.login(email='user@gmail.com', password='password')
    session = client.session
    cart = Cart(client)
    cart.add(product=product, quantity=2)

    cart.coupon_id = coupon.pk
    session[settings.CART_SESSION_ID] = cart.cart
    session['coupon_id'] = coupon.pk
    session.save()
    return client

@pytest.fixture
def admin_client_with_cart(db, client, product, coupon, admin_user):
    client.login(email='admin_user@gmail.com', password='admin_password')
    session = client.session
    cart = Cart(client)
    cart.add(product=product, quantity=2)
    cart.coupon_id = coupon.pk
    session[settings.CART_SESSION_ID] = cart.cart
    session['coupon_id'] = coupon.pk
    session.save()
    return client

@pytest.fixture
def client_with_recommendations(db, client, products, coupon, user):
    client.login(email='user@gmail.com', password='password')
    session = client.session
    cart = Cart(client)
    cart.add(product=products[0], quantity=1)
    cart.add(product=products[1], quantity=1)
    cart.add(product=products[2], quantity=1)
    cart.coupon_id = coupon.pk
    session[settings.CART_SESSION_ID] = cart.cart
    session['coupon_id'] = coupon.pk
    session.save()
    return client

@pytest.fixture
def order(db, user, coupon):
    return Order.objects.create(
        user=user,
        address='home1',
        first_name='John',
        last_name='Doe',
        city='Test City',
        email='user@example.com',
        paid=False,
        coupon=coupon,
        discount=10
    )

@pytest.fixture
def order_items(db, order, product):
    return Order_Item.objects.create(
        product=product,
        order=order,
        price=product.price,
        quantity=2
    )
