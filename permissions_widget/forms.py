"""
Form widget and field.

PermissionSelectMultipleField
    An optionnal form field purely for your own convenience.

PermissionSelectMultipleWidget
    The actual permissions widget.
"""
from django import forms
from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Permission

from .settings import EXCLUDE_APPS, EXCLUDE_MODELS


class PermissionSelectMultipleWidget(forms.CheckboxSelectMultiple):
    """
    Child of CheckboxSelectMultiple which renders
    `permissions_widget/widget.html` to display the form field.
    """
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        table = []
        row = None
        last_app = None
        last_model = None
        permission_types = []

        for permission in self.choices.queryset:
            codename = permission.codename
            permission_type = codename.split('_')[0]
            app = permission.content_type.app_label

            model = permission.content_type.model_class()
            # is it an obsolete contenttype ?
            if model is None:
                continue
            model = model._meta.verbose_name

            if app in EXCLUDE_APPS:
                continue

            if u'%s.%s' % (app, model) in EXCLUDE_MODELS:
                continue

            if permission_type not in permission_types:
                permission_types.append(permission_type)

            if last_model != model or last_app != app:
                if row:
                    table.append(row)
                row = dict(model=model, app=app, permissions={})

            # place permission
            row['permissions'][permission_type] = {
                'value': permission.pk,
            }

            last_app = app
            last_model = model

        t = get_template('permissions_widget/widget.html')
        c = template.Context({
            'name': name,
            'value': value,
            'table': table,
            'permission_types': permission_types,
        })
        return mark_safe(t.render(c))


class PermissionSelectMultipleField(forms.ModelMultipleChoiceField):
    """
    Simple child of forms.ModelMultipleChoiceField which pre-sets
    queryset=Permission.objects.all(). It's an optionnal item here for your
    convenience.
    """
    widget = PermissionSelectMultipleWidget

    def __init__(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = Permission.objects.all()
        super(PermissionSelectMultipleField, self).__init__(queryset, *args,
                **kwargs)
