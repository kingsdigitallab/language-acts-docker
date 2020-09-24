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
            'title',
            'lemma'
        ]

    language = fields.KeywordField(type="keyword")
    first_letter = fields.KeywordField(type="keyword")
    page_url = fields.TextField()

    def prepare_page_url(self, instance):
        parent = instance.get_ancestors().last()
        if parent:
            return parent.url+'?toggler_open={}#page-{}'.format(
                instance.pk, instance.pk)
        return ''

    def prepare_first_letter(self, instance):
        return instance.lemma.upper()[0] if instance.lemma else None

    def prepare_language(self, instance):
        return (instance.specific.language.name
                if instance.specific.language else None)
