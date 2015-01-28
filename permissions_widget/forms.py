"""
Form widget and field.

PermissionSelectMultipleField
    An optionnal form field purely for your own convenience.

PermissionSelectMultipleWidget
    The actual permissions widget.
"""
from string import lower
from django import forms
from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Permission
import itertools

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
        permission_types = {}

        for permission in self.choices.queryset:
            codename = permission.codename
            model_part = "_" + permission.content_type.model
            permission_type = codename
            if permission_type.endswith(model_part):
                permission_type = permission_type[:-len(model_part)]
            app = permission.content_type.app_label

            setattr(permission, "permission_type", permission_type)
            setattr(permission, "value", permission.pk)

            model_class = permission.content_type.model_class()
            model_verbose_name = model_class._meta.verbose_name if model_class else None

            if app in EXCLUDE_APPS:
                continue

            if u'%s.%s' % (app, lower(model_class.__name__)) in EXCLUDE_MODELS:
                continue

            permission_types.setdefault(permission_type, [])
            permission_types[permission_type].append(permission)

            is_app_or_model_different = last_model != model_class or last_app != app
            if is_app_or_model_different:
                row = dict(model=model_verbose_name, model_class=model_class, app=app, permissions={})

            # place permission
            row['permissions'][permission_type] = {
                'value': permission.pk,
                'name': permission.name,
            }

            if is_app_or_model_different:
                table.append(row)

            last_app = app
            last_model = model_class

        permission_types_standard = {k: v for k, v in permission_types.iteritems() if len(v) > 1}
        permission_types_custom = [p for p in itertools.chain(*[v[1] for v in permission_types.iteritems()]) if p.permission_type not in permission_types_standard]

        t = get_template('permissions_widget/widget.html')
        c = template.Context({
            'name': name,
            'value': value,
            'table': table,
            'permission_types': permission_types_standard,
            'permission_types_custom': permission_types_custom,
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
