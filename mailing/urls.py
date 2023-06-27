from mailing.apps import MailingConfig
from django.urls import path

from mailing.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    # path('', MailingListView.as_view(), name='mailing_list'),
    # path('create/', MailingCreateView.as_view(), name='mailing_create'),
    # path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    # path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
]
