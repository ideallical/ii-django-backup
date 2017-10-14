"""
Settings for ideallical drf pagination are all namespaced in the
II_DJANGO_BACKUP setting.
For example your project's `settings.py` file might look like this:

II_DJANGO_BACKUP = {
    'DIR': '/var/backups/',
    'DROPBOX_ACCESS_TOKEN': '**********',
    'DROPBOX_DIR': '/websitename/staging/',
    'USE_GZIP': True,
}

This module provides the `backup_setting` object, that is used to access
ideallical Django backup settings, checking for user settings first, then
falling back to the defaults.
"""
from __future__ import unicode_literals

import os
from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed
from django.utils import six

try:
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
except AttributeError:
    backup_dir = None


DEFAULTS = {
    'DIR': backup_dir,
    'NAME_GENERATOR_FUNC': 'ii_django_backup.name_generators.default',
    'DROPBOX_ACCESS_TOKEN': None,
    'DROPBOX_DIR': None,
    'USE_GZIP': True,
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'NAME_GENERATOR_FUNC',
)


# List of settings that have been removed
REMOVED_SETTINGS = ()


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '{}' for backup setting '{}'. {}: {}.".format(
            val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class BackupSettings(object):
    """
    A settings object, that allows Backup settings to be accessed as
    properties.
    For example:

        from ii_django_backup.settings import backup_settings
        print(backup_settings.DIR)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'II_DJANGO_BACKUP', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Backup setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://github.com/ideallical/ii-django-backup/"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '{}' setting has been removed. Please refer to '{}' "
                    "for available settings.".format(setting, SETTINGS_DOC))
        return user_settings


backup_settings = BackupSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_backup_settings(*args, **kwargs):
    global backup_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'II_DJANGO_BACKUP':
        backup_settings = BackupSettings(
            value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_backup_settings)
