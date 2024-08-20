from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product


# Create your models here.

# User = get_user_model()
#
# class Cart(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.product.name} - {self.quantity}'
#
#     class Meta:
#         ordering = ('-date',)