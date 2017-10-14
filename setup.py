from setuptools import setup

setup(
    name='ii_django_backup',
    version='0.1',
    description='ideallical django backup',
    url='https://github.com/ideallical/ii-django-backup',
    download_url=('https://github.com/ideallical/ii-django-backup/archive/'
                  '0.1.tar.gz'),
    author='ideallical',
    author_email='info@ideallical.com',
    keywords=['django', 'backup', 'dropbox'],
    license='BSD',
    install_requires=[
        'dropbox>=7.1.1',
    ],
    packages=['ii_django_backup'],
    zip_safe=False
)
