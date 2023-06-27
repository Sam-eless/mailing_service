from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config.settings import EMAIL_HOST_USER


def send_verify_email(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }

    email_body = f"Подтвердите свой адрес электронной почты, перейдя по ссылке: " \
                 f"http://{context['domain']}/users/verify_email/{context['uid']}/{context['token']}/"
    send_mail(
        subject='Подтверждение адреса электронной почты',
        message=email_body,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
