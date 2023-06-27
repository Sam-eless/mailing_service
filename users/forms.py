from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordResetForm, \
    SetPasswordForm
from django import forms
from django.core.exceptions import ValidationError

from mailing.forms import FormStyleMixin
from users.models import User
from users.utils import send_verify_email


class UserAuthenticationForm (AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                raise self.get_invalid_login_error()

            if self.user_cache.is_email_verified is False:
                send_verify_email(self.request, self.user_cache)
                raise ValidationError(
                    'Email не верифицирован, проверьте свою почту',
                    code="invalid_login",
                )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'phone', 'avatar', 'country', 'email', 'password1', 'password2')
        fields = ('email', 'password1', 'password2')


class CustomPasswordResetForm(FormStyleMixin, PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User


class CustomSetPasswordForm(FormStyleMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Meta:
            model = User
