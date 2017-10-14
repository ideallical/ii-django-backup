# ideallical django backup

[![pypi-version]][pypi]

## Requirements

* Python (3.5)

## Installation

Install using `pip`...

    pip install ii-django-backup


## Running

    python manage.py backup_database


## Configuration

Configure ii-django-backup in your Django settings:

```python
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

[pypi-version]: https://img.shields.io/pypi/v/ii-django-backup.svg
[pypi]: https://pypi.python.org/pypi/ii-django-backup
