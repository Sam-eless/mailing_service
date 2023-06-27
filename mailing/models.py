from django.db import models
from django.utils.timezone import now

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='почта', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    # created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='кем создан',
    #                                related_name='client')
    is_active = models.BooleanField(default=True, verbose_name='активен')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    ONCE = 'один раз'  # временно
    DAILY = 'раз в день'
    WEEKLY = 'раз в неделю'
    MONTHLY = 'раз в месяц'

    FREQUENCY_CHOICES = [
        (ONCE, 'один раз'),
        (DAILY, 'раз в день'),
        (WEEKLY, 'раз в неделю'),
        (MONTHLY, 'раз в месяц'),
    ]

    CREATED = 'Создана'
    LAUNCHED = 'Запущена'
    COMPLETED = 'Завершена'

    SELECT_STATUS = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    date_of_creation = models.DateTimeField(default=now, verbose_name='Дата создания')
    # scheduled_time = models.DateTimeField(default=None, verbose_name='Время рассылки')
    scheduled_time = models.TimeField(auto_now_add=False, verbose_name='Время рассылки')
    frequency = models.CharField(max_length=14, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, default='Создана', choices=SELECT_STATUS, verbose_name='Статус')
    clients = models.ManyToManyField(Client)
    title = models.CharField(max_length=50, verbose_name='Название рассылки', **NULLABLE)

    # message = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.CASCADE, **NULLABLE)

    # owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Кем создана', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        # permissions = [
        #     ('set_mailing_status', 'Can set mailing status'),
        # ]


class Message(models.Model):
    subject = models.CharField(max_length=254, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    date_of_creation = models.DateTimeField(default=now, verbose_name='дата создания')
    mailing = models.ForeignKey(Mailing, verbose_name='рассылка', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Attempt(models.Model):
    DELIVERED = 'delivered'
    NOT_DELIVERED = 'not_delivered'

    STATUS = (
        (DELIVERED, 'доставлено'),
        (NOT_DELIVERED, 'не доставлено'),
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    time_of_sent = models.DateTimeField(default=now, verbose_name='Время рассылки')
    status = models.CharField(choices=STATUS, verbose_name='Статус')
    response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f"{self.sending.message.subject} - {self.sent_at}"

    class Meta:
        verbose_name = 'Статистика (попытка)'
        verbose_name_plural = 'Статистики (попытки)'
