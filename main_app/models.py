from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, email, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('email must be entered')
        else:
            email = self.normalize_email(email)
            is_superuser = extra_fields.get('is_superuser')
            is_staff = extra_fields.get('is_staff')
            user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, is_superuser=is_superuser, is_staff=is_staff)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, password, email, username=None, first_name=None, last_name=None, **extra_fields):
        username = input("Enter username: ")
        first_name = input('Enter first name: ')
        last_name = input('Enter last name: ')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, password, email, first_name, last_name, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(verbose_name=_('username') ,max_length=100, unique=False)
    email = models.EmailField(verbose_name=_('email') ,unique=True)
    avatar = models.ImageField(verbose_name=_('avatar') ,upload_to='avatars/', blank=True)
    first_name = models.CharField(verbose_name=_('first name') ,max_length=100)
    last_name = models.CharField(verbose_name=_('last name') ,max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
