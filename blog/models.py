from django.db import models
from django.utils.timezone import now

from mailing.models import NULLABLE


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='posts/', verbose_name='изображение', default="posts/nophoto.png")
    date_of_creation = models.DateTimeField(default=now, verbose_name='дата создания')
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title}'

    def increment_count_view(self):
        self.number_of_views += 1
        self.save()

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('-date_of_creation',)
