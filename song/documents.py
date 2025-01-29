from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from song.models import Line


@registry.register_document
class LineDocument(Document):
    class Index:
        name = 'lines'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Line

        fields = [
            'line',
        ]
