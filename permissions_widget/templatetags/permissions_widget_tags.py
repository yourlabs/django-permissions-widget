from django import template

register = template.Library()


@register.filter
def get_for_model(d, row):
    return [o for o in d if o.content_type.model_class() == row['model_class']]

@register.filter
def get_item(d, key):
    return d.get(key, None)
