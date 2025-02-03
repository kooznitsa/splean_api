from typing import Any

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from album.models import Album
from album.repositories import AlbumRepository
from album.v1.serializers import AlbumSerializer, AlbumWithSongsSerializer
from common.pagination import StandardPagination
from common.views import MultiSerializerViewSet


@extend_schema(tags=['albums'])
@extend_schema_view(
    list=extend_schema(description='List all albums'),
    retrieve=extend_schema(description='Get album by ID'),
    songs=extend_schema(description='Get album songs'),
)
class AlbumViewSet(MultiSerializerViewSet):
    serializer_class = AlbumSerializer
    model = serializer_class.Meta.model
    queryset = Album.objects.all()
    pagination_class = StandardPagination
    serializers = {
        'songs': AlbumWithSongsSerializer,
    }

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
        parameters=[
            OpenApiParameter(
                name='id',
                description='List album songs by album ID',
                required=True,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample('Example 1', value=1),
                ],
                location=OpenApiParameter.PATH,
            ),
        ],
    )
    @action(methods=('get',), detail=False, url_path=r'(?P<id>\d+)/songs')
    def songs(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pk = self.kwargs.get('id', None)
        self.queryset = AlbumRepository.get_album_songs(pk)
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=('get',), detail=False, url_path='stats')
    def stats(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return JsonResponse(AlbumRepository.get_stats(), safe=False)
