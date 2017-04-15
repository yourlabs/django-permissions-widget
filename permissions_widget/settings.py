"""
Settings for permissions_widget.

DEFAULT_PERMISSIONS
    Tuple of default (or common) permissions for all models. They will be
    displayed in separate table column. Custom permissions which are not in this
    tuple will be stacked together in one (last) column.
EXCLUDE_APPS
    The permissions widget will exclude any permission for any model in any app
    in the EXCLUDE_APPS list. It contains sensible defaults which you can
    override: sessions, admin and contenttypes for example, as in most cases
    users won't even have the possibility of adding/changing/deleting sessions,
    logentries and content types so why even bother proposing permissions for
    them ? This would just confuse the admin.
    Can be overridden in settings.PERMISSIONS_WIDGET_EXCLUDE_APPS.
EXCLUDE_MODELS
    The permissions widget will exclude any permission for any listed model.
    Models should be listed in the form of `app.model`.
    Can be overridden in settings.PERMISSIONS_WIDGET_EXCLUDE_MODELS.
APPS_ONLY
    The permissions widget will only include permissions for models of the apps
    in the APPS_ONLY list.
    Can be overridden in settings.PERMISSIONS_WIDGET_APPS_ONLY.
MODELS_ONLY
    The permissions widget will only include permissions for listed models.
    Models should be listed in the form of `app.model`.
    Can be overridden in settings.PERMISSIONS_WIDGET_MODELS_ONLY.
PATCH_GROUPADMIN
    If True, `permissions_widget.admin` will override the registered GroupAdmin
    form's user_permission field to use this widget for permissions.
    Can be overridden (ie. to False) in
    settings.PERMISSIONS_WIDGET_PATCH_GROUPADMIN.
PATCH_USERADMIN
    If True, `permissions_widget.admin` will override the registered UserAdmin
    form's user_permission field to use this widget for permissions.
    Can be overridden (ie. to False) in
    settings.PERMISSIONS_WIDGET_PATCH_USERADMIN.
"""
from django.conf import settings

try:
    # Django 1.7
    from django.db.models.options import Options
    default_django_permissions = Options.default_permissions
except (ImportError, AttributeError):
    default_django_permissions = ('add', 'change', 'delete')


DEFAULT_PERMISSIONS = getattr(settings, 'PERMISSIONS_WIDGET_DEFAULT_PERMISSIONS',
      default_django_permissions)
EXCLUDE_APPS = getattr(settings, 'PERMISSIONS_WIDGET_EXCLUDE_APPS', [
    'sites', 'reversion', 'contenttypes', 'admin', 'sessions',
    'easy_thumbnails',])
EXCLUDE_MODELS = getattr(settings, 'PERMISSIONS_WIDGET_EXCLUDE_MODELS', [
    'auth.permission',])
APPS_ONLY = getattr(settings, 'PERMISSIONS_WIDGET_APPS_ONLY', None)
MODELS_ONLY = getattr(settings, 'PERMISSIONS_WIDGET_MODELS_ONLY', None)
PATCH_USERADMIN = getattr(settings, 'PERMISSIONS_WIDGET_PATCH_USERADMIN', True)
PATCH_GROUPADMIN = getattr(settings, 'PERMISSIONS_WIDGET_PATCH_GROUPADMIN',
                           True)
