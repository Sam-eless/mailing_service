from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission

NULLABLE = {'blank': True, 'null': True}


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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                "can_view_all_user",
                "Сan view user"
            ),
            (
                "can_change_all_user",
                "Сan change user"
            )
        ]


manager_group, created = Group.objects.get_or_create(name='Менеджеры')
if created:
    # Создание прав доступа для группы модераторов

    # Право на просмотр всех рассылок
    can_view_any_mailings = Permission.objects.get(codename='can_view_any_mailings')
    manager_group.permissions.add(can_view_any_mailings)

    # Право отключение рассылок
    can_disable_mailings = Permission.objects.get(codename='can_disable_mailings')
    manager_group.permissions.add(can_disable_mailings)

    # Права управления пользователями
    can_view_all_user = Permission.objects.get(codename='can_view_all_user')
    manager_group.permissions.add(can_view_all_user)

    can_change_all_user = Permission.objects.get(codename='can_change_all_user')
    manager_group.permissions.add(can_change_all_user)
