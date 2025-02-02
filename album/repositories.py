from album.models import Album


class AlbumRepository:
    @staticmethod
    def get_album_songs(album_id: int | None) -> list:
        return Album.objects.filter(id=album_id).order_by('name') if album_id else []
