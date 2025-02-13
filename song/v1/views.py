from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from common.pagination import StandardPagination
from common.views import MultiSerializerViewSet
from song.models import Song
from song.repositories import SongRepository
from song.v1.serializers import SongSerializer, SongWithLinesSerializer


@extend_schema(tags=['songs'])
@extend_schema_view(
    list=extend_schema(description='List all songs'),
    retrieve=extend_schema(description='Get song by ID'),
    lines=extend_schema(description='Get song lines'),
    by_year=extend_schema(description='List songs with specific year'),
)
class SongViewSet(MultiSerializerViewSet):
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = Song.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializers = {
        'lines': SongWithLinesSerializer,
        'by_year': SongSerializer,
    }

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
    @action(methods=('get',), detail=False, url_path=r'(?P<id>\d+)/lines')
    def lines(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pk = self.kwargs.get('id', None)
        self.queryset = SongRepository.get_song_lines(pk)
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
        self.queryset = SongRepository.get_songs_within_year(year)
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=('get',), detail=False, url_path='stats')
    def stats(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return JsonResponse(SongRepository.get_stats(), safe=False)
