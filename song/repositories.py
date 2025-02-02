from album.models import Album
from song.models import Song


class SongRepository:
    @staticmethod
    def get_songs_within_year(year: int | None) -> list:
        if year:
            album_ids = Album.objects.filter(date__year=year).values_list('id', flat=True)
            return Song.objects.filter(album__id__in=album_ids).order_by('name')
        return []

    @staticmethod
    def get_song_lines(song_id: int | None) -> list:
        return Song.objects.filter(id=song_id).order_by('name') if song_id else []
