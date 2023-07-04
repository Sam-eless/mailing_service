from django.db import models
from config import settings
from django.utils.timezone import now


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='почта', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='кем создан', **NULLABLE)
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
    start_date = models.DateField(default=now, verbose_name='Дата начала рассылки')
    end_date = models.DateField(default=now, verbose_name='Дата окончания рассылки', **NULLABLE)
    frequency = models.CharField(max_length=14, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, default='Создана', choices=SELECT_STATUS, verbose_name='Статус')
    clients = models.ManyToManyField(Client)
    title = models.CharField(max_length=50, verbose_name='Название рассылки', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кем создана', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                "can_view_any_mailings",
                "Сan view any mailings"
            ),
            (
                "can_disable_mailings",
                "Can disable mailings"
            )]


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
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус')
    response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):

        return f"{message.subject} - {self.time_of_sent}"

    def get_email(self):
        message = Message.objects.get(mailing=self.mailing)
        # client = Client.objects.get(mailing=self.mailing)
        client = self.mailing.clients.first()
        return f'{client.email}'

    class Meta:
        verbose_name = 'Попытка отправки'
        verbose_name_plural = 'Попытки отправки'

