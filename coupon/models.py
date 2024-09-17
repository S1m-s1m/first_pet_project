from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()

class Coupon(models.Model):
    code = models.CharField(verbose_name=_('code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(verbose_name=_('valid from'))
    valid_to = models.DateTimeField(verbose_name=_('valid to'))
    discount = models.IntegerField(verbose_name=_('discount'), validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(verbose_name=_('active'))
    max_uses = models.PositiveIntegerField(default=1, verbose_name=_('max uses'))
    used_count = models.PositiveIntegerField(default=0, verbose_name=_('used count'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
