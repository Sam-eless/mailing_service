from django.core.management import BaseCommand
import django_rq
import time
from django.utils import timezone
from mailing.services.cron import once_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        once_mailing()
