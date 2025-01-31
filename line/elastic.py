from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool


class ElasticsearchQueryManager:
    @staticmethod
    def query_lines_containing_word(word: str) -> Bool:
        return Q(
            'bool',
            should=[Q('match', line=word)],
            minimum_should_match=1,
        )
