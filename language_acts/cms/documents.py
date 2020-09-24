from cms.models.pages import (
    RecordEntry
)
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class RecordEntryDocument(Document):
    class Index:
        name = 'language_acts'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = RecordEntry

        fields = [
            'title'
        ]

    language = fields.KeywordField(type="keyword")
    first_letter = fields.KeywordField(type="keyword")
    page_url = fields.TextField()

    def prepare_page_url(self, instance):
        return instance.url

    def prepare_first_letter(self, instance):
        return instance.title.upper()[0] if instance.title else None

    def prepare_language(self, instance):
        return (instance.specific.language.name
                if instance.specific.language else None)
