from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Stay


@registry.register_document
class DocumentStay(Document):
    class Index:
        name = 'main'
        search = {'number_of_shards': 1, 'number_of_replicas': 0}

    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    slug = fields.TextField(
        attr='slug',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.TextField()
        })

    class Django:
        model = Stay
