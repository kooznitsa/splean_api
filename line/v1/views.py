import logging
import random
from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from common.pagination import StandardPagination
from line.documents import LineDocument
from line.elastic import ElasticsearchQueryManager
from line.models import Line
from line.v1.serializers import LineSerializer

info_logger = logging.getLogger('info_logger')


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
        responses={status.HTTP_200_OK: serializer_class},
    )
    @action(methods=('get',), detail=False, url_path='random')
    def random(self, request: Request, *args: Any, **kwargs: Any):
        self.queryset = random.choices(self.get_queryset(), k=1)
        return super().list(request, *args, **kwargs)
