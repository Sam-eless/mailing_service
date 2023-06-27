from django.contrib.auth.models import AbstractUser
from django.db import models
from mailing.models import NULLABLE
from django.contrib.auth.models import Group, Permission


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    is_email_verified = models.BooleanField(verbose_name='email подтвержден', default=False)
    is_blocked = models.BooleanField(verbose_name='пользователь заблокирован', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# moderator_group, created = Group.objects.get_or_create(name='Менеджеры')
# if created:
#     # Создание прав доступа для группы модераторов
#
#     # Право на отмену публикации продукта
#     can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')
#     moderator_group.permissions.add(can_unpublish_product)
#
#     # Право на изменение описания продукта
#     can_change_description_any_product = Permission.objects.get(codename='can_change_description_any_product')
#     moderator_group.permissions.add(can_change_description_any_product)
#
#     # Право на изменение категории продукта
#     can_change_category_any_product = Permission.objects.get(codename='can_change_category_any_product')
#     moderator_group.permissions.add(can_change_category_any_product)

