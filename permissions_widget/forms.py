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

from .settings import EXCLUDE_APPS, EXCLUDE_MODELS, DEFAULT_PERMISSIONS


class PermissionSelectMultipleWidget(forms.CheckboxSelectMultiple):
    """
    Child of CheckboxSelectMultiple which renders
    `permissions_widget/widget.html` to display the form field.
    """

    custom_permission_types = []

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        t = get_template('permissions_widget/widget.html')
        c = template.Context({
            'name': name,
            'value': value,
            'table': self.get_table(),
            'default_permission_types': DEFAULT_PERMISSIONS,
            'custom_permission_types': self.custom_permission_types
        })
        return mark_safe(t.render(c))

    def get_table(self):
        table = []
        row = None
        last_app = None
        last_model = None

        for permission in self.choices.queryset:
            codename = permission.codename
            model_part = "_" + permission.content_type.model
            permission_type = codename
            if permission_type.endswith(model_part):
                permission_type = permission_type[:-len(model_part)]
            app = permission.content_type.app_label

            model_class = permission.content_type.model_class()
            model_class_name = lower(model_class.__name__) if model_class else None
            model_verbose_name = model_class._meta.verbose_name if model_class else None

            if app in EXCLUDE_APPS:
                continue

            if model_class_name and u'%s.%s' % (app, model_class_name) in EXCLUDE_MODELS:
                continue

            if permission_type not in list(DEFAULT_PERMISSIONS) + self.custom_permission_types:
                self.custom_permission_types.append(permission_type)

            is_app_or_model_different = last_model != model_class or last_app != app
            if is_app_or_model_different:
                row = dict(model=model_verbose_name, model_class=model_class, app=app, permissions={})

            row['permissions'][permission_type] = permission

            if is_app_or_model_different:
                table.append(row)

            last_app = app
            last_model = model_class

        return table


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
