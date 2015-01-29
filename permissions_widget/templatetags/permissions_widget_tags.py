from django import template
from django.utils.translation import ugettext

register = template.Library()


@register.filter
def get_item(d, key):
    return d.get(key, None)


@register.filter(name='translate')
def translate(text):
    return ugettext(text)
