from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from common.pagination import StandardPagination
from common.serializers import MultiSerializerViewSet
from song.managers import SongManager
from song.models import Song
from song.v1.serializers import SongSerializer, SongWithLinesSerializer


class SongViewSet(MultiSerializerViewSet):
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = Song.objects.all().order_by('id')
    pagination_class = StandardPagination
    is_serialized_with_children = False

    def get_serializer_class(self):
        return SongWithLinesSerializer if self.is_serialized_with_children else SongSerializer

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
        parameters=[
            OpenApiParameter(
                name='id',
                description='List song lines by song ID',
                required=True,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample('Example 1', value=1),
                ],
                location=OpenApiParameter.PATH,
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path='(?P<id>\d+)/lines')
    def lines(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pk = self.kwargs.get('id', None)
        self.queryset = SongManager.get_song_lines(pk)
        self.is_serialized_with_children = True
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
        parameters=[
            OpenApiParameter(
                name='year',
                description='Filter songs by album year',
                required=True,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample('Example 1', value=1999),
                ],
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path='by-year')
    def by_year(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        year = self.request.query_params.get('year', None)
        self.queryset = SongManager.get_songs_within_year(year)
        return super().list(request, *args, **kwargs)
