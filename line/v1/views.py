import logging
import random
from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from common.pagination import StandardPagination
from line.elastic import ElasticsearchQueryManager
from line.models import Line
from line.v1.serializers import LineSerializer

info_logger = logging.getLogger('info_logger')


@extend_schema(tags=['lines'])
@extend_schema_view(
    list=extend_schema(description='List all lines'),
    retrieve=extend_schema(description='Get line by ID'),
    by_word=extend_schema(description='Get lines containing word'),
    random=extend_schema(description='Get random line'),
    alcohol=extend_schema(description='Get lines referring to alcohol'),
    petersburg=extend_schema(description='Get lines referring to Petersburg'),
    winter=extend_schema(description='Get lines referring to winter'),
)
class LineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LineSerializer
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
    def by_word(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        word = self.request.query_params.get('word', None)
        query = ElasticsearchQueryManager.query_lines_containing_word(word)
        self.queryset = ElasticsearchQueryManager().perform_search(query, word)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
    )
    @action(methods=('get',), detail=False, url_path='alcohol')
    def alcohol(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        query = ElasticsearchQueryManager.query_alcohol_lines()
        self.queryset = ElasticsearchQueryManager().perform_search(query, 'alcohol')
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
    )
    @action(methods=('get',), detail=False, url_path='petersburg')
    def petersburg(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        query = ElasticsearchQueryManager.query_petersburg_lines()
        self.queryset = ElasticsearchQueryManager().perform_search(query, 'petersburg')
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class(many=True)},
    )
    @action(methods=('get',), detail=False, url_path='winter')
    def winter(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        query = ElasticsearchQueryManager.query_winter_lines()
        self.queryset = ElasticsearchQueryManager().perform_search(query, 'winter')
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class},
    )
    @action(methods=('get',), detail=False, url_path='random')
    def random(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ids = Line.cached_objects.values_from_cache('id').get('values')
        queryset = self.get_queryset().filter(id=random.choice(ids))[0]
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
