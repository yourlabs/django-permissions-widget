from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter
def get_item(d, key):
    return d.get(key, None)


@register.filter(name='translate')
def translate(text):
    return gettext(text)
