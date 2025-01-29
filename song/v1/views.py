from typing import Any, Type

from django.db.models import QuerySet, Case, When, Value, IntegerField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.serializers import Serializer

from song.managers import SongManager
from song.models import Line, Song
from song.v1.serializers import LineSerializer, SongSerializer


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = Song.objects.all().order_by('-name')
    pagination_class = None

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class},
        parameters=[
            OpenApiParameter(
                name='year',
                description='Filter songs by year',
                required=True,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample('Example 1', value=1999),
                ],
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path='by-year')
    def filter_by_year(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        year = self.request.query_params.get('year', None)
        songs = SongManager.get_songs_within_year(year)
        serializer = self.get_serializer(songs, many=True)

        return JsonResponse(serializer.data, safe=False)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class},
        parameters=[
            OpenApiParameter(
                name='word',
                description='Filter lines by words',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample('Example 1', value='мёд'),
                ],
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path='by-words')
    def filter_by_words(self, request: Request, *args: Any, **kwargs: Any):
        word = self.request.query_params.get('word', None)
        songs = SongManager.get_songs_containing_words(word)
        return JsonResponse(songs, many=True)
        # serializer = self.get_serializer(songs, many=True)
        #
        # return JsonResponse(serializer.data, safe=False)
