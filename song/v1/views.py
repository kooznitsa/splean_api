import logging
from typing import Any

from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request

from song.documents import LineDocument
from song.managers import ElasticsearchQueryManager, LineManager, SongManager
from song.models import Line, Song
from song.v1.serializers import LineSerializer, SongSerializer

info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


class StandardPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'page_size'
    offset_query_param = 'page'
    max_limit = 100


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = Song.objects.all().order_by('id')
    pagination_class = StandardPagination

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
    def by_year(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        year = self.request.query_params.get('year', None)
        self.queryset = SongManager.get_songs_within_year(year)
        return super().list(request, *args, **kwargs)


class LineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LineSerializer
    document_class = LineDocument
    model = serializer_class.Meta.model
    queryset = Line.objects.prefetch_related('song').order_by('song__album__date', 'id')
    pagination_class = StandardPagination

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
        parameters=[
            OpenApiParameter(
                name='word',
                description='Filter song lines by word or phrase',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample('Example 1', value='мёд'),
                ],
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path='by-word')
    def by_word(self, request: Request, *args: Any, **kwargs: Any):
        word = self.request.query_params.get('word', None)
        query = ElasticsearchQueryManager.query_lines_containing_word(word)
        search = self.document_class.search().query(query)
        response = search.execute()
        info_logger.info(f"Found {response.hits.total.value} hit(s) for query: '{word}'")
        self.queryset = search.to_queryset()
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
        parameters=[
            OpenApiParameter(
                name='song_id',
                description='List song lines by song ID',
                required=True,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample('Example 1', value=1),
                ],
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path='by-song')
    def by_song(self, request: Request, *args, **kwargs):
        song_id = self.request.query_params.get('song_id', None)
        self.queryset = LineManager.get_lines_by_song_id(song_id)
        return super().list(request, *args, **kwargs)
