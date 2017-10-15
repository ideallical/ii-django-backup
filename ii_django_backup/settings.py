"""
Settings for ideallical django backup are all namespaced in the
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

from django.conf import settings

from ii_django_package_settings.settings import PackageSettings

try:
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
except AttributeError:
    backup_dir = None


class BackupSettings(PackageSettings):
    NAME = 'II_DJANGO_BACKUP'
    DOC = 'https://github.com/ideallical/ii-django-package-settings/'
    DEFAULTS = {
        'DIR': backup_dir,
        'NAME_GENERATOR_FUNC': 'ii_django_backup.name_generators.default',
        'DROPBOX_ACCESS_TOKEN': None,
        'DROPBOX_DIR': None,
        'USE_GZIP': True,
    }
    IMPORT_STRINGS = ('NAME_GENERATOR_FUNC', )


backup_settings = BackupSettings(None)
