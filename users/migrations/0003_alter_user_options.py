# Generated by Django 4.2.2 on 2023-06-27 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_blocked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('view_service_users', 'View service users')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
