from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from catalog.models import Product
from coupon.models import Coupon
from django.utils.translation import gettext_lazy as _

from pet_project import settings

User = get_user_model()

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    address = models.CharField(verbose_name=_('address'), max_length=100)
    first_name = models.CharField(verbose_name=_('first name'),max_length=100)
    last_name = models.CharField(verbose_name=_('last name'),max_length=100)
    city = models.CharField(verbose_name=_('city'),max_length=100)
    email = models.EmailField(verbose_name=_('email'),)
    paid = models.BooleanField(verbose_name=_('paid'),default=False)
    created = models.DateTimeField(verbose_name=_('created'),auto_now=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('coupon'))
    discount = models.IntegerField(verbose_name=_('discount'),default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stripe_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return str(self.pk)

    def total_order_cost(self):
        total_cost = sum(item.total_item_cost() for item in self)
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def __iter__(self):
        for item in Order_Item.objects.filter(order=self):
            yield item

    def get_stripe_url(self):
        if not self.stripe_id:
        # никаких ассоциированных платежей
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
        # путь Stripe для тестовых платежей
            path = '/test/'
        else:
        # путь Stripe для настоящих платежей
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.coupon.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost_before_discount(self):
        return sum(item.total_item_cost() for item in self.items.all())

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

class Order_Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, verbose_name=_('product'))
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_('order'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=1)

    def __str__(self):
        return str(self.pk)

    def total_item_cost(self):
        return self.price * self.quantity

    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

#set PATH=%PATH%;%SystemRoot%\system32;C:\Users\Максим\Downloads\gettext\bin

# django-admin makemessages --all внесение слов
# makemessages: Эта команда создает файлы перевода
# .po для всех текстовых строк, помеченных для перевода
# в коде вашего Django приложения. Она анализирует
# исходный код приложения, находит все строки,
# которые должны быть переведены, и создает
# соответствующие файлы .po или слова для перевода

# django-admin compilemessages применение перевода слов
# Эта команда компилирует файлы перевода .po
# в бинарные файлы формата .mo, которые Django
# может использовать для перевода текста на другие языки.
# Это необходимо для того, чтобы Django мог
# эффективно загружать и использовать переводы
# во время выполнения. Команда обычно вызывается после того,
# как были внесены или изменены переводы,
# чтобы обновить бинарные файлы перевода.
