from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from django.urls import path
from . import views
from blog.views import PostListView, PostDetailView, index

app_name = BlogConfig.name

urlpatterns = [
    path('<int:pk>/', cache_page(60)(PostDetailView.as_view()), name='post_detail'),
    path('', views.index, name='index'),
]
