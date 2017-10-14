def default(db_dict, dt):
    db_name = db_dict['NAME']
    engine = db_dict['ENGINE']

    if engine in ['django.db.backends.postgresql_psycopg2',
                  'django.contrib.gis.db.backends.postgis']:
        extension = '.backup'
    else:
        extension = '.sql'

    return '{time}_db_backup-{db_name}{extension}'.format(
        time=dt.strftime('%Y.%m.%d.%H.%M.%S'),
        db_name=db_name,
        extension=extension
    )
