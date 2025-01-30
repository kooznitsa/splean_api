from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool

from song.models import Album, Song


class SongManager:
    @staticmethod
    def get_songs_within_year(year: int | None) -> list:
        if year:
            album_ids = Album.objects.filter(date__year=year).values_list('id', flat=True)
            return Song.objects.filter(album__id__in=album_ids).order_by('name')
        return []


class ElasticsearchQueryManager:
    @staticmethod
    def query_lines_containing_word(word: str) -> Bool:
        return Q(
            'bool',
            should=[Q('match', line=word)],
            minimum_should_match=1,
        )
