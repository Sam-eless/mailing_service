from django.core.management import BaseCommand
# from django_rq_scheduler import scheduler
import django_rq
import time
from django.utils import timezone
from mailing.services.cron import scheduled_mailing, schedule_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduled_mailing()
        # schedule_mailing()
        # self.stdout.write(self.style.SUCCESS('Mailing scheduled successfully.'))

        # python -Xutf8 manage.py dumpdata catalog -o catalog_data.json
        # python manage.py migrate catalog zero
        # python manage.py makemigrations
        # python manage.py migrate
        # python manage.py fill
