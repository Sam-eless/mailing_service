import schedule
import time
from django.core.mail import send_mail
from django.utils import timezone
from mailing.models import *
from django.conf import settings

def scheduled_mailing():
    now = timezone.now()
    mailings = Mailing.objects.filter(
        start_date__lte=now.date(),  # Рассылка должна начаться до или в текущую дату
        end_date__gte=now.date()  # Рассылка должна закончиться после или в текущую дату
    )

    for mailing in mailings:
        if mailing.status == Mailing.LAUNCHED:
            continue

        message = mailing.message
        clients = mailing.clients.all()

        if mailing.frequency == Mailing.ONCE:
            # Рассылка "один раз"
            if mailing.start_date <= now.date() <= mailing.end_date:
                # Отправляем письма только в промежутке между start_date и end_date
                for client in clients:
                    try:
                        send_mail(
                            message.subject,
                            message.message,
                            settings.EMAIL_HOST_USER,
                            [client.email],
                            fail_silently=False,
                        )

                        Attempt.objects.create(
                            mailing=mailing,
                            time_of_sent=now,
                            status=Attempt.DELIVERED,
                            response='Письмо успешно отправлено'
                        )

                    except Exception as e:
                        Attempt.objects.create(
                            mailing=mailing,
                            time_of_sent=now,
                            status=Attempt.NOT_DELIVERED,
                            response=str(e)
                        )

                mailing.status = Mailing.LAUNCHED
                mailing.save()

        elif mailing.frequency == Mailing.DAILY:
            # Рассылка "ежедневно"
            if mailing.start_date <= now.date() <= mailing.end_date:
                # Отправляем письма только в промежутке между start_date и end_date
                for client in clients:
                    if Attempt.objects.filter(mailing=mailing, status=Attempt.DELIVERED, client=client).exists():
                        # Если была отправлена рассылка клиенту сегодня, пропускаем отправку
                        continue

                    try:
                        send_mail(
                            message.subject,
                            message.message,
                            settings.EMAIL_HOST_USER,
                            [client.email],
                            fail_silently=False,
                        )

                        Attempt.objects.create(
                            mailing=mailing,
                            client=client,
                            time_of_sent=now,
                            status=Attempt.DELIVERED,
                            response='Письмо успешно отправлено'
                        )

                    except Exception as e:
                        Attempt.objects.create(
                            mailing=mailing,
                            client=client,
                            time_of_sent=now,
                            status=Attempt.NOT_DELIVERED,
                            response=str(e)
                        )

                mailing.status = Mailing.LAUNCHED
                mailing.save()

        elif mailing.frequency == Mailing.WEEKLY:
            # Рассылка "еженедельно"
            weekday = now.weekday()  # Возвращает день недели в виде числа (0 - понедельник, 6 - воскресенье)
            weekdays = dict(
                zip(range(7), ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']))
            weekday_name = weekdays[weekday]

            if mailing.start_date <= now.date() <= mailing.end_date and getattr(mailing, weekday_name):
                # Отправляем письма только в промежутке между start_date и end_date и в соответствии с выбранным днем недели
                for client in clients:
                    if Attempt.objects.filter(mailing=mailing, status=Attempt.DELIVERED, client=client).exists():
                        # Если была отправлена рассылка клиенту сегодня, пропускаем отправку
                        continue

                    try:
                        send_mail(
                            message.subject,
                            message.message,
                            settings.EMAIL_HOST_USER,
                            [client.email],
                            fail_silently=False,
                        )

                        Attempt.objects.create(
                            mailing=mailing,
                            client=client,
                            time_of_sent=now,
                            status=Attempt.DELIVERED,
                            response='Письмо успешно отправлено'
                        )

                    except Exception as e:
                        Attempt.objects.create(
                            mailing=mailing,
                            client=client,
                            time_of_sent=now,
                            status=Attempt.NOT_DELIVERED,
                            response=str(e)
                        )

                mailing.status = Mailing.LAUNCHED
                mailing.save()

        elif mailing.frequency == Mailing.MONTHLY:
            # Рассылка "ежемесячно"
            if mailing.start_date <= now.date() <= mailing.end_date and now.day == 1:
                # Отправляем письма только в промежутке между start_date и end_date в первый день месяца

                for client in clients:

                    if Attempt.objects.filter(mailing=mailing, status=Attempt.DELIVERED, client=client).exists():
                        # Если была отправлена рассылка клиенту в этом месяце, пропускаем отправку
                        continue
                    try:
                        send_mail(
                            message.subject,
                            message.body,
                            'sender@example.com',
                            [client.email],
                            fail_silently=False,
                        )
                        Attempt.objects.create(
                            mailing=mailing,
                            client=client,
                            time_of_sent=now,
                            status=Attempt.DELIVERED,
                            response='Email sent successfully'
                        )
                    except Exception as e:

                        Attempt.objects.create(
                            mailing=mailing,
                            client=client,
                            time_of_sent=now,
                            status=Attempt.NOT_DELIVERED,
                            response=str(e)
                        )

                mailing.status = Mailing.LAUNCHED
                mailing.save()


def run_mailing():
    scheduled_mailing()


# Запускаем функцию scheduled_mailing() ежедневно в 10:00 утра
schedule.every().day.at("14:47").do(run_mailing)

while True:
    schedule.run_pending()
    time.sleep(1)
    print(timezone.now())

#
# Да, вы можете использовать Django RQ Scheduler для запуска периодических задач в Django.
#
# Django RQ Scheduler - это расширение для Django RQ, которое позволяет запускать периодические задачи на основе расписания, используя библиотеку schedule. Для использования Django RQ Scheduler вам необходимо установить его с помощью pip:
#
# Copy
# pip install django-rq-scheduler
# Затем вы можете настроить RQ Scheduler в файле settings.py вашего Django-проекта:
#
# python
# Copy
# INSTALLED_APPS = [
#     # ... другие приложения ...
#     'django_rq',
#     'django_rq_scheduler',
# ]
#
# RQ_QUEUES = {
#     'default': {
#         'HOST': 'localhost',
#         'PORT': 6379,
#         'DB': 0,
#     },
# }
#
# SCHEDULER_AUTOSTART = True
# Здесь мы добавляем django_rq и django_rq_scheduler в список INSTALLED_APPS нашего проекта и настраиваем Redis-очередь для использования с RQ. Мы также устанавливаем SCHEDULER_AUTOSTART в True, чтобы RQ Scheduler автоматически запускался при запуске нашего приложения.
#
# Теперь вы можете определить свою периодическую задачу и зарегистрировать ее в RQ Scheduler. Например, вы можете создать файл tasks.py и определить задачу send_email:
#
# python
# Copy
# from django.core.mail import send_mail
# from django.utils import timezone
# from datetime import datetime, timedelta
#
# def send_email():
#     now = timezone.now()
#     subject = f'Email sent at {now}'
#     message = 'This is a test email.'
#     from_email = 'example@example.com'
#     recipient_list = ['recipient@example.com']
#     send_mail(subject, message, from_email, recipient_list)
#
# # Запускаем задачу ежедневно в 10:00 утра
# from django_rq_scheduler import scheduler
#
# scheduler.schedule(
#     scheduled_time=datetime.utcnow(),
#     func=send_email,
#     interval=86400,  # 24 часа в секундах
#     repeat=None
# )
# Здесь мы импортируем модуль scheduler из django_rq_scheduler и используем его для запуска задачи send_email ежедневно в 10:00 утра, используя параметры scheduled_time, interval и repeat.
#
# Надеюсь, это поможет!