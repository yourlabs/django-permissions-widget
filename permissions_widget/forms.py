"""
Form widget and field.

PermissionSelectMultipleField
    Permission field handling EXCLUDE_APPS and EXCLUDE_MODELS
    settings.

PermissionSelectMultipleWidget
    The actual permissions widget.
"""
from django import forms
from django import template
from django.db.models import Q
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
            # get permission type from codename
            codename = permission.codename
            model_part = "_" + permission.content_type.model
            permission_type = codename
            if permission_type.endswith(model_part):
                permission_type = permission_type[:-len(model_part)]

            # get app label and model verbose name
            app = permission.content_type.app_label
            model_class = permission.content_type.model_class()
            model_verbose_name = model_class._meta.verbose_name if model_class else None

            if permission_type not in list(DEFAULT_PERMISSIONS) + self.custom_permission_types:
                self.custom_permission_types.append(permission_type)

            # each row represents one model with its permissions categorized by type
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

        # exclude models and apps by settings
        exclude_models_q = Q()
        for exclude_model in EXCLUDE_MODELS:
            app_label, model = exclude_model.split('.')
            exclude_models_q |= Q(
                content_type__app_label=app_label,
                content_type__model=model
            )
        queryset = queryset.exclude(
            Q(content_type__app_label__in=EXCLUDE_APPS) |
            exclude_models_q
        )

        super(PermissionSelectMultipleField, self).__init__(queryset, *args,
                **kwargs)
