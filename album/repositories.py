from django.db.models import Count

from album.models import Album


class AlbumRepository:
    @staticmethod
    def get_album_songs(album_id: int | None) -> list:
        return Album.objects.filter(id=album_id).order_by('name') if album_id else []

    @staticmethod
    def get_stats() -> dict:
        albums_by_date = Album.objects.order_by('date')
        albums_by_songs = Album.objects.annotate(count=Count('song')).order_by('-count')
        albums_by_duration = Album.objects.order_by('-duration')

        return {
            'oldest': {
                'name': albums_by_date.first().name,
                'date': albums_by_date.first().date,
            },
            'newest': {
                'name': albums_by_date.last().name,
                'date': albums_by_date.last().date,
            },
            'largest': {
                'name': albums_by_songs.first().name,
                'num_songs': albums_by_songs.first().count,
            },
            'smallest': {
                'name': albums_by_songs.last().name,
                'num_songs': albums_by_songs.last().count,
            },
            'longest': {
                'name': albums_by_duration.first().name,
                'duration': albums_by_duration.first().duration,
            },
            'shortest': {
                'name': albums_by_duration.last().name,
                'duration': albums_by_duration.last().duration,
            },
        }
