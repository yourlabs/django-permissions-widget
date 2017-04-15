from crispy_forms.layout import Field
from crispy_forms.utils import TEMPLATE_PACK
from django.contrib.auth.models import Permission
from permissions_widget.forms import PermissionSelectMultipleWidget, filter_permissions
from .settings import DEFAULT_PERMISSIONS


class PermissionWidget(Field):
    """
    Layout object. It contain table of defined permissions.

    Examples::

        PermissionTable('user_permissions', queryset=Permission.objects.filter(app="my_app")
    """

    template = "permissions_widget/crispy_field.html"
    custom_permission_types = []
    groups_permissions = []

    def __init__(self, *args, **kwargs):
        super(PermissionWidget, self).__init__(*args, **kwargs)
        self.widget = PermissionSelectMultipleWidget()
        self.widget.queryset = kwargs['queryset'] if 'queryset' in kwargs else Permission.objects.select_related()
        self.widget.queryset = filter_permissions(self.widget.queryset)
        self.widget.groups_permissions = kwargs['groups_permissions'] if 'groups_permissions' in kwargs else []

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}

        extra_context['table'] = self.widget.get_table()
        extra_context['groups_permissions'] = self.widget.groups_permissions
        extra_context['default_permission_types'] = DEFAULT_PERMISSIONS
        extra_context['custom_permission_types'] = self.widget.custom_permission_types

        return super(PermissionWidget, self).render(form, form_style, context, template_pack, extra_context, **kwargs)
