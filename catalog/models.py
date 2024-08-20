from enum import Enum
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields, TranslatableModel

User = get_user_model()

# Create your models here.

size_choices = [
    ('XXS', 'XX Small'),
    ('XS', 'X Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'X Large'),
    ('XXL', 'XX Large'),
    ('XXXL', 'XXX Large')
]

class Brand(TranslatableModel):
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    name = models.CharField(verbose_name=_('name'), max_length=100, db_index=True)
    translations = TranslatedFields(
        description=models.TextField(verbose_name=_('description'))
    )
    image = models.ImageField(verbose_name=_('image'), upload_to='brand_images/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

class Category(TranslatableModel):
    translations = TranslatedFields(
        slug=models.SlugField(max_length=200, db_index=True, unique=True),
        name=models.CharField(verbose_name=_('name'), max_length=100, db_index=True, unique=True),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Product(TranslatableModel):
    translations = TranslatedFields(
        slug = models.SlugField(max_length=200, db_index=True),
        name = models.CharField(verbose_name=_('name'), max_length=200),
        description = models.TextField(verbose_name=_('description')),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('category'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('brand'), blank=True, null=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    size = models.CharField(verbose_name=_('size'), max_length=100, choices=size_choices, default='M')
    image = models.ImageField(verbose_name=_('image'), upload_to='clothes_images/', blank=True)
    availability = models.BooleanField(verbose_name=_('availability'), default=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, verbose_name=_('product'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name=_('author'))
    text = models.TextField(verbose_name=_('text'))
    date = models.DateTimeField(verbose_name=_('date'), auto_now=True, blank=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), on_delete=models.CASCADE, blank=True, null=True)# blank может быть не заполнено в формах null может быть не заполнено в самой модели и будет заменено на NULL(нужно для date и foreignkeyfield)

    def get_child_reviews(self):
        return Review.objects.filter(parent=self).order_by('date')

    def __str__(self):
        return f"{self.author.username} - {self.product} - {self.date}"

    class Meta:
        ordering = ('-date',)
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
