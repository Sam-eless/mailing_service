from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, MessageForm, MessageDetailForm, ClientForm
from mailing.models import Mailing, Message, Client


# Create your views here.
class MailingListView(ListView):
    model = Mailing
    extra_context = {
        'title': 'Список рассылок'
    }


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageDetailForm, extra=0, can_delete=False)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            MessageFormset = inlineformset_factory(Mailing, Message, form=MessageDetailForm, extra=0, can_delete=False)
            context_data['formset'] = MessageFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingCreateView(CreateView):
    model = Mailing
    # fields = ('title', 'frequency', 'status',)
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Редактирование'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1, max_num=1)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment',)
    # form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Создание рассылки'
    }


class ClientUpdateView(UpdateView):
    model = Client
    # fields = ('first_name', 'last_name', 'email', 'comment',)
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Редактирование'
    }


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:mailing_list')
