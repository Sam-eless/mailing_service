from mailing.apps import MailingConfig
from django.urls import path

from mailing.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]
