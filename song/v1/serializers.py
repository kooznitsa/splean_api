from rest_framework import serializers

from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    """Song detailed info"""
    album_name = serializers.CharField(read_only=True, source='album.name')

    class Meta:
        model = Song
        fields = ('name', 'duration', 'album_name')


class SongWithLinesSerializer(serializers.ModelSerializer):
    """Song with lines"""
    album_name = serializers.CharField(read_only=True, source='album.name')

    class Meta:
        model = Song
        fields = ('name', 'duration', 'album_name', 'line_set')
        depth = 1
