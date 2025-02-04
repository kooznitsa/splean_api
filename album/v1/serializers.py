from rest_framework import serializers

from album.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    """Album detailed info"""
    class Meta:
        model = Album
        fields = ('name', 'date', 'duration')


class AlbumWithSongsSerializer(serializers.ModelSerializer):
    """Album with songs"""
    class Meta:
        model = Album
        fields = ('name', 'date', 'duration', 'song_set')
        depth = 1
