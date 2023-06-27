from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.core.cache import cache
from blog.models import Post
from mailing.models import Mailing


class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Список постов'
    }


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        post_id = self.kwargs['pk']
        cache_key = f'post_{post_id}'
        post = cache.get(cache_key)

        if not post:
            post = super().get_object(queryset=queryset)
            post.increment_count_view()
            cache.set(cache_key, post)

        return post

    # def get_object(self, queryset=None):
    #     post = super().get_object(queryset=queryset)
    #     post.increment_count_view()
    #     return post



def index(request):
    # Получаем количество рассылок всего
    total_mailings = Mailing.objects.count()

    # Получаем количество активных рассылок
    active_mailing = Mailing.objects.filter(is_active=True).count()

    # Получаем количество уникальных клиентов для рассылок
    unique_clients = Mailing.objects.values('clients').distinct().count()

    # Получаем 3 случайные статьи из блога
    random_post = Post.objects.order_by('?')[:3]

    # Передаем полученную информацию в шаблон
    context = {
        'total_mailings': total_mailings,
        'active_mailing': active_mailing,
        'unique_clients': unique_clients,
        'random_post': random_post,
        'title': 'Главная страница'
    }
    return render(request, 'index.html', context=context)
