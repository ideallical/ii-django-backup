import datetime
import os
import subprocess  # nosec

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import dropbox
from dropbox.exceptions import AuthError
from ii_django_backup.settings import backup_settings as bs


class Command(BaseCommand):
    help = 'Make backup of Django database'

    def check(self):
        """
        Check if ii-django-backup is configured properly.

        :return: None
        :raises CommandError: if ii-django-backup is not configured correctly
        """
        backup_dir = bs.DIR
        dropbox_dir = bs.DROPBOX_DIR
        dropbox_access_token = bs.DROPBOX_ACCESS_TOKEN
        use_dropbox = (dropbox_dir is not None) or (
            dropbox_access_token is not None)

        if backup_dir is None:
            raise CommandError(
                'Please declare II_DJANGO_BACKUP[\'DIR\'], as the default '
                'backup dir is based on settings.BASE_DIR, and your settings '
                'don\'t define a BASE_DIR.')

        if use_dropbox and (dropbox_dir is None):
            raise CommandError(
                'Please declare II_DJANGO_BACKUP[\'DROPBOX_DIR\'] or disable '
                'using dropbox by setting II_DJANGO_BACKUP[\'DROPBOX_ACCESS_'
                'TOKEN\'] to None')

        if use_dropbox and (dropbox_access_token is None):
            raise CommandError(
                'Please declare II_DJANGO_BACKUP[\'DROPBOX_ACCESS_TOKEN\'] or '
                'disable using dropbox by setting II_DJANGO_BACKUP[\'DROPBOX_D'
                'IR\'] to None')

    def get_backup_command(self, db_dict, backup_path):
        """
        Return backup shell command for given database dict and path.

        :param dict db_dict: used database information
        :param str backup_path: used path to export backup to

        :return: the backup command string
        :rtype: str
        :raises CommandError: if the db_dict['ENGINE'] is unknown
        """
        db_type = db_dict['ENGINE']
        # set default HOST
        if db_dict['HOST'] in ['', None]:
            db_dict['HOST'] = 'localhost'

        if db_type in ['django.db.backends.postgresql_psycopg2',
                       'django.contrib.gis.db.backends.postgis']:

            # set default Postgres PORT
            if db_dict['PORT'] in ['', None]:
                db_dict['PORT'] = 5432

            cmd = ('pg_dump -U {USER} -h {HOST} -p {PORT} -Fc {NAME}'
                   ' --no-owner').format(**db_dict)

        elif db_type == 'django.db.backends.mysql':

            # set default MySQL PORT
            if db_dict['PORT'] in ['', None]:
                db_dict['PORT'] = 3306

            cmd = (
                'mysqldump --opt -Q -h {HOST} -P {PORT} -u {USER} '
                '{NAME}').format(**db_dict)
        else:
            raise CommandError(
                'No backup command is implemented for {}'.format(db_type))

        if bs.USE_GZIP:
            return '{cdm} | gzip > {backup_path}'.format(
                cdm=cmd, backup_path=backup_path)

        return '{cdm} > {backup_path}'.format(cdm=cmd, backup_path=backup_path)

    def handle(self, *args, **options):
        """
        Creates backup for Django's default database connection.
        If configured, it will also upload this backup to the given dropbox
        folder.

        :return: None
        :raises CommandError: if ii-django-backup is not configured correctly
        :raises CommandError: if the db_dict['ENGINE'] is unknown
        :raises CommandError: if script couldn't connect to Dropbox
        """
        self.check()

        # gather configuration variables
        db_dict = settings.DATABASES['default']

        # create an unique backup filename
        filename = bs.NAME_GENERATOR_FUNC(db_dict=db_dict,
                                          dt=datetime.datetime.now())

        # when using GZIP, add .gz extension to the filename
        if bs.USE_GZIP:
            filename = '{}.gz'.format(filename)

        backup_dir = bs.DIR
        backup_path = os.path.join(backup_dir, filename)

        # create backup-dir if it doesn't exists yet
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)

        # backup locally
        cmd = self.get_backup_command(db_dict, backup_path)
        subprocess.call(cmd, shell=True)  # nosec

        # backup to dropbox if needed
        if bs.DROPBOX_ACCESS_TOKEN is not None:
            try:
                dbx = dropbox.Dropbox(bs.DROPBOX_ACCESS_TOKEN)
                with open(backup_path, 'rb') as f:
                    data = f.read()
                    dbx.files_upload(data, '{}{}'.format(
                        bs.DROPBOX_DIR, filename))
            except AuthError:
                raise CommandError(
                    'Could not connect to Dropbox. Please check II_DJANGO_BAC'
                    'KUP[\'DROPBOX_TOKEN\'].')
