from django import template

register = template.Library()


@register.simple_tag()
def media_path(path):
    return f'../../media/{path}/'


@register.filter
def media_path(path):
    return f'../../media/{path}/'
