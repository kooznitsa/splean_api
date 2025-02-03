from django.conf import settings
from django.core.management import call_command
import environ
import pytest
from rest_framework.test import APIClient

env = environ.Env()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_TEST_HOST'),
        'PORT': env.str('POSTGRES_TEST_PORT'),
        'ATOMIC_REQUESTS': True,
    }

    with django_db_blocker.unblock():
        call_command('loaddata', 'albums.json')
        call_command('loaddata', 'songs.json')
        for i in range(1, 13):
            call_command('loaddata', f'{i}.json')


@pytest.fixture
def api_client():
    return APIClient()
