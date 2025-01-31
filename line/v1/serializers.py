from rest_framework import serializers

from line.models import Line


class LineSerializer(serializers.ModelSerializer):
    """Line detailed info"""
    song_name = serializers.CharField(read_only=True, source='song.name')

    class Meta:
        model = Line
        fields = ('line', 'song_name')
