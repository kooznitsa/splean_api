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


@pytest.fixture
def song_files():
    text_1 = """
    В Петербурге мы сойдемся снова,
    Словно солнце мы похоронили в нем,
    И блаженное, бессмысленное слово
    В первый раз произнесем.
    В черном бархате советской ночи,
    В бархате всемирной пустоты,
    Все поют блаженных жен родные очи,
    Все цветут бессмертные цветы.

    Дикой кошкой горбится столица,
    На мосту патруль стоит,
    Только злой мотор во мгле промчится
    И кукушкой прокричит.
    Мне не надо пропуска ночного,
    Часовых я не боюсь:
    За блаженное, бессмысленное слово
    Я в ночи советской помолюсь.
    """

    text_2 = """
    Я вернулся в мой город, знакомый до слез,
    До прожилок, до детских припухлых желез.

    Ты вернулся сюда, так глотай же скорей
    Рыбий жир ленинградских речных фонарей,

    Узнавай же скорее декабрьский денек,
    Где к зловещему дегтю подмешан желток.

    Петербург! я еще не хочу умирать!
    У тебя телефонов моих номера.

    Петербург! У меня еще есть адреса,
    По которым найду мертвецов голоса.

    Я на лестнице черной живу, и в висок
    Ударяет мне вырванный с мясом звонок,

    И всю ночь напролет жду гостей дорогих,
    Шевеля кандалами цепочек дверных.
    """

    _write_to_file(text_1, '1111')
    _write_to_file(text_2, '1112')


def _write_to_file(text: str, filename: str):
    with open(f'{settings.INPUT_TXT_PATH}{filename}.txt', 'w', encoding='utf-8') as f:
        f.write(text)
