from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel
# from wagtail.core.models import Orderable
# from wagtail.snippets.edit_handlers import SnippetChooserPanel
# from modelcluster.fields import ParentalKey


@register_snippet
class LemmaLanguage(index.Indexed, models.Model):
    name = models.CharField(max_length=128)
    orderno = models.IntegerField(default=0)

    panels = [
        FieldPanel('name'),
        FieldPanel('orderno'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    class Meta:
        verbose_name = "Lemma Language"
        verbose_name_plural = "Lemma Languages"

        ordering = ['orderno']

    def __str__(self):
        return self.name


@register_snippet
class POSLabel(index.Indexed, models.Model):
    name = models.CharField(max_length=256)

    panels = [
        FieldPanel('name'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    class Meta:
        verbose_name = "Eagle POS Label"
        verbose_name_plural = "Eagle POS Labels"

    def __str__(self):
        return self.name


@register_snippet
class GlossaryItem(models.Model):
    term = models.CharField(max_length=256)
    description = models.TextField()

    panels = [
        FieldPanel('term'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Glossary term"
        verbose_name_plural = "Glossary terms"

    def __str__(self):
        return self.term


@register_snippet
class BibliographyItem(models.Model):
    author = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)

    panels = [
        FieldPanel('author'),
        FieldPanel('title'),
        FieldPanel('publisher'),
    ]

    class Meta:
        verbose_name = "Glossary term"
        verbose_name_plural = "Glossary terms"

    def __str__(self):
        return "{}. {}".format(self.author, self.title)
