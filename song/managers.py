from song.documents import LineDocument
from song.models import Album, Song


class SongManager:
    @staticmethod
    def get_songs_within_year(year: int | None) -> list:
        if year:
            album_ids = Album.objects.filter(date__year=year).values_list('id', flat=True)
            return Song.objects.filter(album__id__in=album_ids).order_by('name')
        return []

    @staticmethod
    def get_songs_containing_words(word: str) -> list:
        return LineDocument.search().query('match', line=word)
        # if lines := LineDocument.search().query('match', line=word):
        #     song_ids = {i.song_id for i in lines}
        #     return Song.objects.filter(id__in=song_ids).order_by('name')
        # return []
