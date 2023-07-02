from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from mailing.models import Mailing, Client, Message, Attempt
from django.conf import settings

from datetime import datetime
from django.utils import timezone


def once_mailing():
    # Получаем все рассылки, которые должны быть запущены в текущий момент или в будущем
    mailings = Mailing.objects.filter(start_date__lte=timezone.now(), is_active=True)
    for mailing in mailings:
        if mailing.status == 'Создана' or mailing.status == 'Запущена':
            # Проверяем, нужно ли запустить рассылку
            if mailing.end_date is None or mailing.end_date >= timezone.now().date():
                mailing.status = 'Запущена'
                mailing.save()
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
                                                             status=Attempt.DELIVERED,
                                                             response='Письмо успешно отправлено')
                            attempt.save()
                            if mailing.frequency == Mailing.ONCE:
                                mailing.status = Mailing.COMPLETED
                                mailing.is_active = False
                                mailing.save()

                            print(f'Сообщение успешно отправлено. Попытка отправки {attempt.id} создана.')

                    except Exception as e:
                        # Записываем статистику об ошибке
                        attempt = Attempt.objects.create(mailing=mailing, time_of_sent=timezone.now(),
                                                         status=Attempt.NOT_DELIVERED, response=str(e))
                        attempt.save()
                        print(f'Сообщение не было отправлено. Попытка отправки {attempt.id} создана.')


def weekly_mailing():
    # Получаем все рассылки, которые должны быть запущены в текущий момент или в будущем
    mailings = Mailing.objects.filter(frequency=Mailing.WEEKLY, is_active=True)
    for mailing in mailings:
        if mailing.status == 'Создана' or mailing.status == 'Запущена':
            # Проверяем, нужно ли запустить рассылку
            if mailing.end_date is None or mailing.end_date >= timezone.now().date():
                mailing.status = 'Запущена'
                mailing.save()
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
                                                             status=Attempt.DELIVERED,
                                                             response='Письмо успешно отправлено')
                            attempt.save()

                            print(f'Сообщение успешно отправлено. Попытка отправки {attempt.id} создана.')

                    except Exception as e:
                        # Записываем статистику об ошибке
                        attempt = Attempt.objects.create(mailing=mailing, time_of_sent=timezone.now(),
                                                         status=Attempt.NOT_DELIVERED, response=str(e))
                        attempt.save()
                        print(f'Сообщение не было отправлено. Попытка отправки {attempt.id} создана.')
            if mailing.end_date <= timezone.now().date():
                mailing.status = Mailing.COMPLETED
                mailing.is_active = False
                mailing.save()



def monthly_mailing():
    # Получаем все рассылки, которые должны быть запущены в текущий момент или в будущем
    mailings = Mailing.objects.filter(frequency=Mailing.MONTHLY, is_active=True)
    for mailing in mailings:
        print(mailing.status)
        print(mailing.title)
        if mailing.status == 'Создана' or mailing.status == 'Запущена':
            # Проверяем, нужно ли запустить рассылку
            if mailing.end_date is None or mailing.end_date >= timezone.now().date():
                mailing.status = 'Запущена'
                mailing.save()
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
                                                             status=Attempt.DELIVERED,
                                                             response='Письмо успешно отправлено')
                            attempt.save()

                            print(f'Сообщение успешно отправлено. Попытка отправки {attempt.id} создана.')

                    except Exception as e:
                        # Записываем статистику об ошибке
                        attempt = Attempt.objects.create(mailing=mailing, time_of_sent=timezone.now(),
                                                         status=Attempt.NOT_DELIVERED, response=str(e))
                        attempt.save()
                        print(f'Сообщение не было отправлено. Попытка отправки {attempt.id} создана.')
            if mailing.end_date <= timezone.now().date():
                mailing.status = Mailing.COMPLETED
                mailing.is_active = False
                mailing.save()
