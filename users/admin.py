from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

    def ready(self):
        User.create_manager_group_and_permissions()
        # Получаем разрешение для модели User
