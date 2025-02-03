from django.db.models import Count

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

    @staticmethod
    def get_stats() -> dict:
        songs_by_lines = Song.objects.annotate(count=Count('line')).filter(count__gt=0).order_by('-count')
        songs_by_duration = Song.objects.order_by('-duration')

        return {
            'longest_by_lines': {
                'name': songs_by_lines.first().name,
                'num_lines': songs_by_lines.first().count,
            },
            'shortest_by_lines': {
                'name': songs_by_lines.last().name,
                'num_lines': songs_by_lines.last().count,
            },
            'longest_by_duration': {
                'name': songs_by_duration.first().name,
                'duration': songs_by_duration.first().duration,
            },
            'shortest_by_duration': {
                'name': songs_by_duration.last().name,
                'duration': songs_by_duration.last().duration,
            },
        }
