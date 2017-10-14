# ideallical django backup

[![pypi-version]][pypi]

## Requirements

* Python (3.5)

## Installation

Install using `pip`...
```shell
$ pip install ii-django-backup
```

## Running
```shell
$ python manage.py backup_database
```

## Configuration

Configure ii-django-backup in your Django settings:

```python
INSTALLED_APPS = {
    [..],
    'ii_django_backup',
    [..],
}

II_DJANGO_BACKUP = {
    'DIR': '/var/backups/',
    'DROPBOX_ACCESS_TOKEN': '**********',
    'DROPBOX_DIR': '/websitename/staging/',
    'USE_GZIP': True,
}
```

Setting `II_DJANGO_BACKUP['DIR']` to `'/var/backups/'` let's ii-django-backup
know where to store your backups locally.
By default this is set to `os.path.join(settings.BASE_DIR, 'backups')`; this
requires `BASE_DIR` being defined in your Django settings.

Setting `II_DJANGO_BACKUP['DROPBOX_ACCESS_TOKEN']` to `**********`, enables
backup to Dropbox using this access token. By default this is set to `None`.

Setting `II_DJANGO_BACKUP['DROPBOX_DIR']` to `/websitename/staging/` let's
ii-django-backup know where to store your backups at Dropbox.
By default this is set to `None`.

Setting `II_DJANGO_BACKUP['USE_GZIP']` to `True` enables Gzipping the backup
file. By default this is set to `True`.

# Trouble shooting
Note that passwords are NOT sent over the commandline (for security reasons).
Therefor you need to make sure the mysqldump and pgdump commands know your
database's password to do backups without password prompt.

For Postgres:

either create a `.pgpass` file in your home-directory and chmod it 600.
The content could look like this:

```t
localhost:5432:database_name:username:secretPassword
```

or set an ENV named PGPASSWORD with your Postgres database password. For Heroku you would be able to do this like so:

```shell
$ heroku config:set PGPASSWORD=secretPassword
```

For MySQL:

Create a `.my.cnf` file in your home-directory and chmod it 600.
The content could look like this:

```t
[mysqldump]
user=username
password=secretPassword

[client]
user=username
password=secretPassword
```

[pypi-version]: https://img.shields.io/pypi/v/ii-django-backup.svg
[pypi]: https://pypi.python.org/pypi/ii-django-backup
