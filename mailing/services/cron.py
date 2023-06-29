# import schedule
# from django_rq_scheduler import scheduler
# from datetime import datetime, timedelta
# import time
# import django_rq
# from django.core.mail import send_mail
# from django.utils import timezone
# from django_rq import enqueue
# from mailing.models import *
# from django.conf import settings
from datetime import datetime

# def scheduled_mailing():


from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from mailing.models import Mailing, Client, Message, Attempt
from django.conf import settings

from datetime import datetime
from django.utils import timezone


def scheduled_mailing():
    # Получаем все рассылки, которые должны быть запущены в текущий момент или в будущем
    mailings = Mailing.objects.filter(start_date__lte=timezone.now(), is_active=True)
    for mailing in mailings:
        # Проверяем, нужно ли запустить рассылку
        if mailing.end_date is None or mailing.end_date >= timezone.now().date():
            # Получаем список клиентов, которым нужно отправить сообщение
            clients = mailing.clients.all()
            for client in clients:
                try:
                    if client.email is not None:
                        # Отправляем сообщение
                        message = Message.objects.get(mailing=mailing)
                        send_mail(
                            message.subject,
                            message.message,
                            settings.EMAIL_HOST_USER,
                            [client.email],
                            fail_silently=False,
                        )
                        # Записываем статистику
                        attempt = Attempt.objects.create(mailing=mailing, time_of_sent=timezone.now(),
                                                         status=Attempt.DELIVERED, response='Письмо успешно отправлено')
                        attempt.save()
                except Exception as e:
                    # Записываем статистику об ошибке
                    attempt = Attempt.objects.create(mailing=mailing, time_of_sent=timezone.now(),
                                                     status=Attempt.NOT_DELIVERED, response=str(e))
                    attempt.save()
