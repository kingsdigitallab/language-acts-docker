from cms.models.pages import (
    RecordPage, RecordEntry
)
from django_elasticsearch_dsl import Document, TextField
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class RecordPageDocument(Document):
    class Index:
        name = 'language_acts'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = RecordPage

        fields = [
            'title',
        ]

        language = TextField()

        def prepare_language(self, obj):
            return (obj.specific.language.name
                    if obj.specific.language else None)


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

        language = TextField()
        first_letter = TextField()

        def prepare_first_letter(self, obj):
            return obj.title.upper()[0] if obj.title else None

        def prepare_language(self, obj):
            return [entry.specific.language.name for entry in
                    obj.get_children() if entry.specific.language is
                    not None]
