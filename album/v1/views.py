from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from album.managers import AlbumManager
from album.models import Album
from album.v1.serializers import AlbumSerializer, AlbumWithSongsSerializer
from common.pagination import StandardPagination
from common.serializers import MultiSerializerViewSet


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
    is_serialized_with_children = False

    def get_serializer_class(self):
        return AlbumWithSongsSerializer if self.is_serialized_with_children else AlbumSerializer

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
    @action(methods=('get',), detail=False, url_path='(?P<id>\d+)/songs')
    def songs(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pk = self.kwargs.get('id', None)
        self.queryset = AlbumManager.get_album_songs(pk)
        self.is_serialized_with_children = True
        return super().list(request, *args, **kwargs)
