from django.db.models import Count

from album.models import Album


class AlbumRepository:
    @staticmethod
    def get_album_songs(album_id: int | None) -> list:
        return Album.objects.filter(id=album_id).order_by('name') if album_id else []

    @staticmethod
    def get_stats() -> dict:
        oldest = Album.objects.order_by('date').first()
        newest = Album.objects.order_by('date').last()
        counted_songs = Album.objects.annotate(count=Count('song')).order_by('-count')
        max_songs = counted_songs.first()
        min_songs = counted_songs.last()

        return {
            'oldest': {'name': oldest.name, 'date': oldest.date},
            'newest': {'name': newest.name, 'date': newest.date},
            'largest_album': {
                'name': max_songs.name,
                'num_songs': max_songs.count,
            },
            'smallest_album': {
                'name': min_songs.name,
                'num_songs': min_songs.count,
            },
        }
