.. image:: https://pypip.in/d/django-permissions-widget/badge.png
    :target: https://crate.io/packages/django-permissions-widget
.. image:: https://pypip.in/v/django-permissions-widget/badge.png   
    :target: https://crate.io/packages/django-permissions-widget

By default, Django's admin provides a permission widget which looks like this:

.. image:: http://permissions-widget.readthedocs.org/en/latest/_static/images/default_widget.png

There are several problems with this widget:

- the permission description is cut, see the fourth line:
  'admin_test_autocomplete | bar | Can add l'. The administrator will not be
  able to read it and might report it as a bug.
- it proposes permissions for `admin.logentry`. The administrator will not
  understand what this is about and will ask you about it.
- it uses a widget which might be new to the administrator and he might ask how
  to use it.

The purpose of this app is to provide a better widget for selecting permissions
as well as an easy way to replace the default permissions widget in your admin
site. It will look like this:

.. image:: http://permissions-widget.readthedocs.org/en/latest/_static/images/new_widget.png

Requirements
------------

- Maintained against Python 2.7
- and Django 1.5

Quick Install
-------------

- Install the latest release via: `pip install django-permissions-widget`.
- Add to `settings.INSTALLED_APPS`, after `django.contrib.admin` which we want
  to override: `'permissions_widget',`. If you are using custom user modeal as 
  for Django 1.5 - you have to add `'permissions_widget',` after the app, that 
  contains your custom user model.

That's it ! You should have a sane permissions widget now.

Resources
---------

- `Documentation graciously hosted
  <http://permissions-widget.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_, read the complete documentation.
- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_, subscribe to it to be informed about potential
  backward compatibility breaks (after 1.0.0 release).
- `Git graciously hosted
  <https://github.com/yourlabs/django-permissions-widget/>`_ by `GitHub
  <http://github.com>`_, report bugs and request pulls.
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-permissions-widget/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_, install via pip.
