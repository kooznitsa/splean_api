import logging

from django.db.models import QuerySet
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool

from line.documents import LineDocument
from line.lists import alcohol, petersburg, winter

info_logger = logging.getLogger('info_logger')


class ElasticsearchQueryManager:
    SEARCH_SIZE = 1000
    document_class = LineDocument

    @staticmethod
    def query_lines_containing_word(word: str) -> Bool:
        return Q(
            'bool',
            should=[Q('match', line=word)],
            minimum_should_match=1,
        )

    @classmethod
    def query_alcohol_lines(cls) -> Bool:
        return cls.search_by_topics(alcohol.ALCOHOL_DRINKS)

    @classmethod
    def query_petersburg_lines(cls) -> Bool:
        return cls.search_by_topics(petersburg.PETERSBURG)

    @classmethod
    def query_winter_lines(cls) -> Bool:
        return cls.search_by_topics(winter.WINTER)

    @staticmethod
    def search_by_topics(topics: list):
        return Q('multi_match', query=' '.join(topics), fields=['line',])

    def perform_search(self, query: Bool, tag: str) -> QuerySet:
        search = self.document_class.search().extra(size=self.SEARCH_SIZE).query(query)
        response = search.execute()
        info_logger.info(f"Found {response.hits.total.value} hit(s) for query `{tag}`")
        return search.to_queryset()
