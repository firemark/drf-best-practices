from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser

from hello.managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    is_moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='pages')
    title = models.CharField(max_length=50)
    description = models.TextField(default='')

    def __str__(self):
        return self.title


class Notification(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    invoke_on = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='items')
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.category.name}:{self.name}'
