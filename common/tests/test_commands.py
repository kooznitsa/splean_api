import json
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
import pytest

from album.models import Album
from song.models import Song

pytestmark = pytest.mark.django_db


class TestCreateLinesJsonCommand:
    COMMAND = 'createlinesjson'
    FILENAME_1 = '1111'
    FILENAME_2 = '1112'

    def test_createlinesjson_success(self, song_files):
        album = Album.objects.get(id=1)
        Song.objects.bulk_create([
            Song(id=int(self.FILENAME_1), name='Test Song 1', album=album, duration='8:11'),
            Song(id=int(self.FILENAME_2), name='Test Song 2', album=album, duration='8:12'),
        ])

        call_command(self.COMMAND, path=settings.INPUT_TXT_PATH)

        file_1 = f'{settings.OUTPUT_JSON_PATH}{self.FILENAME_1}.json'
        file_2 = f'{settings.OUTPUT_JSON_PATH}{self.FILENAME_2}.json'

        for path in (file_1, file_2):
            assert os.path.exists(path)

        with open(file_1, 'r', encoding='utf-8') as f1, open(file_2, 'r', encoding='utf-8') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
            assert data1[-1]['pk'] == data2[0]['pk'] - 1

        for path in (file_1, file_2):
            os.remove(path)
            assert not os.path.exists(path)

        self._clear_txt_dir()

    def test_createlinesjson_for_nonexistent_songs(self, song_files):
        with pytest.raises(CommandError) as exc_info:
            call_command(self.COMMAND, path=settings.INPUT_TXT_PATH)
            assert type(exc_info.value.__cause__) is CommandError

        for path in (
            f'{settings.OUTPUT_JSON_PATH}{self.FILENAME_1}.json',
            f'{settings.OUTPUT_JSON_PATH}{self.FILENAME_2}.json',
        ):
            assert not os.path.exists(path)

        self._clear_txt_dir()

    def test_createlinesjson_with_wrong_filename(self):
        file_path = f'{settings.INPUT_TXT_PATH}abc.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Test line')

        with pytest.raises(CommandError) as exc_info:
            call_command(self.COMMAND, path=settings.INPUT_TXT_PATH)
            assert type(exc_info.value.__cause__) is CommandError

        os.remove(file_path)

    def _clear_txt_dir(self):
        os.remove(f'{settings.INPUT_TXT_PATH}{self.FILENAME_1}.txt')
        os.remove(f'{settings.INPUT_TXT_PATH}{self.FILENAME_2}.txt')
