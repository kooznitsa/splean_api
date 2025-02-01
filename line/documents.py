from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analysis, analyzer

from line.models import Line
from song.models import Song

russian_stop = analysis.token_filter(
    'russian_stop', type='stop', stopwords='_russian_',
)
russian_stemmer = analysis.token_filter(
    'russian_stemmer', type='stemmer', language='russian',
)

russian_analyzer = analyzer(
    'russian_morphology',
    type='custom',
    tokenizer='standard',
    char_filter='html_strip',
    filter=[
        'lowercase',
        russian_stop,
        russian_stemmer,
    ],
)


@registry.register_document
class LineDocument(Document):
    song = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'album': fields.ObjectField(properties={'name': fields.TextField()}),
        'duration': fields.TextField(),
    })
    line = fields.TextField(required=True, analyzer=russian_analyzer)

    class Index:
        name = 'lines'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Line
        related_models = [Song]

        fields = [
            'id',
        ]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Song):
            return Line.objects.filter(song=related_instance)
