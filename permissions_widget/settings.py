"""
Settings for permissions_widget.

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


EXCLUDE_APPS = getattr(settings, 'PERMISSIONS_WIDGET_EXCLUDE_APPS', [
    'reversion', 'contenttypes', 'admin', 'sessions'])
EXCLUDE_MODELS = getattr(settings, 'PERMISSIONS_WIDGET_EXCLUDE_MODELS', [])
PATCH_USERADMIN = getattr(settings, 'PERMISSIONS_WIDGET_PATCH_USERADMIN', True)
PATCH_GROUPADMIN = getattr(settings, 'PERMISSIONS_WIDGET_PATCH_GROUPADMIN',
                           True)
