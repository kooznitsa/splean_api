from rest_framework import serializers

from song.models import Line, Song


class SongSerializer(serializers.ModelSerializer):
    """Song detailed info"""
    album_name = serializers.CharField(read_only=True, source='album.name')

    class Meta:
        model = Song
        fields = ('name', 'duration', 'album_name')


class LineSerializer(serializers.ModelSerializer):
    """Line detailed info"""
    song_name = serializers.CharField(read_only=True, source='song.name')

    class Meta:
        model = Line
        fields = ('line', 'song_name')
