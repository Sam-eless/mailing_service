from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, MessageForm, MessageDetailForm, ClientForm, MailingFormManager
from mailing.models import Mailing, Message, Client
from users.models import User


# Create your views here.
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        # user1 = User.objects.get(email='iaiznura@gmail.com')
        # permissions = user1.get_all_permissions()
        # print(permissions)
        manager = self.request.user.has_perm("mailing.can_view_any_mailings") and self.request.user.is_authenticated
        if manager:
            return queryset
        else:
            # queryset = queryset.filter(owner=self.request.user, is_active=True)
            queryset = queryset.filter(owner=self.request.user)
            return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
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


class MailingCreateView(LoginRequiredMixin, CreateView):
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
        form.instance.owner = self.request.user if self.request.user.is_authenticated else None
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Редактирование'
    }

    def get_form_class(self):
        class_form = MailingFormManager
        mailing = self.get_object()
        if not self.request.user.has_perm('mailing.can_disable_mailings'):
            class_form = MailingForm
        if self.request.user == mailing.owner:
            class_form = MailingForm
        return class_form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1, max_num=1)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)
        return context_data

    def test_func(self):
        mailing = self.get_object()
        manager = self.request.user.has_perm(
            "mailing.can_view_any_mailings") and self.request.user.has_perm(
            'mailing.can_disable_mailings')
        if manager:
            return True
        else:
            return self.request.user == mailing.owner

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        form.instance.author = self.request.user if self.request.user.is_authenticated else None
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment',)
    # form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь автором этого продукта.")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    # fields = ('first_name', 'last_name', 'email', 'comment',)
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Редактирование'
    }


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:mailing_list')
