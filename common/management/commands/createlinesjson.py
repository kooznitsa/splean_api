import json
import os
from typing import NoReturn

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from line.models import Line
from song.models import Song


class Command(BaseCommand):
    help = """
        Creates JSON files with song lines. Examples:
        - in terminal with default path: make createlinesjson
        - in terminal with parameter: make createlinesjson TXTPATH=/home/app/common/tests/files/
        - in Django code: call_command('createlinesjson', path='/home/app/common/tests/files/')

        .TXT files should be numeric, e.g. 1111.txt. Number (1111) indicates song ID in database.
    """

    def add_arguments(self, parser) -> NoReturn:
        parser.add_argument(
            '--path',
            type=str,
            default=settings.INPUT_TXT_PATH,
            help='Path to .TXT files',
        )

    def handle(self, *args, **options) -> NoReturn:
        start_count = Line.objects.order_by('id').last().id + 1
        files = os.listdir(options['path'])
        for f in files:
            if f.endswith('.txt'):
                song_id = f.strip('.txt')
                self._check_file(song_id, f)
                lines = self._read_file(f)
                json_data = self._process_text(lines, start_count, song_id)
                self._write_to_file(song_id, json_data)
                start_count += len(lines)

    @staticmethod
    def _check_file(song_id: str, f: str) -> NoReturn:
        if not song_id.isnumeric():
            raise CommandError(f'File name {f} should be numeric')
        if not Song.objects.filter(pk=int(song_id)).exists():
            raise CommandError(f'Song with id {song_id} does not exist')

    def _read_file(self, f: str) -> list:
        with open(f'{settings.INPUT_TXT_PATH}{f}', 'r', encoding='utf-8') as fr:
            lines = list(filter(None, map(lambda x: x.strip(), fr.readlines())))
        return lines

    @staticmethod
    def _process_text(lines: list, start_count: int, song_id: int) -> list:
        json_data = []

        for line in lines:
            json_data.append(
                {
                    "model": "line.line",
                    "pk": start_count,
                    "fields": {
                        "line": line,
                        "song": song_id
                    }
                }
            )
            start_count += 1

        return json_data

    def _write_to_file(self, song_id: int, json_data: list) -> NoReturn:
        try:
            with open(f'{settings.OUTPUT_JSON_PATH}{song_id}.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(json_data, indent=2, ensure_ascii=False))
        except Exception as e:
            raise CommandError(f'File could not be created due to error: {e}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created JSON file {song_id}.json')
        )
