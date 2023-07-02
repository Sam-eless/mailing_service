from django import forms

from mailing.models import Mailing, Message, Client


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        # fields = '__all__'
        exclude = ('date_of_creation', 'owner',)


class MailingFormManager(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('is_active',)


class MessageForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MessageDetailForm(FormStyleMixin, forms.ModelForm):
    subject = forms.CharField(label='Тема письма',
                              widget=forms.Textarea(attrs={'cols': 40, 'rows': 2, 'readonly': 'readonly'}))
    message = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'cols': 40, 'rows': 3, 'readonly': 'readonly'}))

    date_of_creation = forms.DateTimeField(label='Дата создания',
                                           widget=forms.Textarea(attrs={'cols': 40, 'rows': 1, 'readonly': 'readonly'}))

    class Meta:
        model = Message
        fields = ('subject', 'message', 'date_of_creation')


class ClientForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Client
        # fields = '__all__'
        exclude = ('date_of_creation', 'owner',)
