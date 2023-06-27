from django.contrib import admin

from mailing.models import Mailing, Client, Message, Attempt


# Register your models here.

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status', 'date_of_creation', 'frequency',)
    search_fields = ('title', 'status',)
    list_filter = ('status', 'frequency',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    # list_filter = ('first_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message',)
    # list_filter = ('created_at',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'time_of_sent', 'status', 'response',)
    list_filter = ('mailing', 'time_of_sent', 'status', 'response',)
