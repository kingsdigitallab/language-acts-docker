from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.core.rich_text import RichText
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


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


"""

Glossary Terms and Bibliography Items

"""


@register_snippet
class GlossaryTerm(index.Indexed, models.Model):
    term = RichTextField(
        null=True, blank=True, editor='bibliography')
    description = RichTextField(
        null=True, blank=True, editor='bibliography')

    panels = [
        FieldPanel('term'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Glossary term"
        verbose_name_plural = "Glossary terms"
        ordering = ['term', ]

    search_fields = [
        index.SearchField('term', partial_match=True),
        index.SearchField('description', partial_match=True),
    ]

    def __str__(self):
        return str(RichText(self.term))


@register_snippet
class BibliographyEntry(index.Indexed, Orderable, models.Model):
    full_citation = RichTextField(
        null=True, blank=True, editor='bibliography')
    reference = RichTextField(
        blank=True, editor='bibliography')

    panels = [
        FieldPanel('reference'),
        FieldPanel('full_citation'),
    ]

    search_fields = [
        index.SearchField('full_citation', partial_match=True),
    ]

    class Meta:
        verbose_name = "Bibliography entry"
        verbose_name_plural = "Bibliography entries"
        ordering = ['full_citation', ]

    def __str__(self):
        return str(RichText(self.reference))


class GlossaryTermItem(index.Indexed, models.Model):
    page = ParentalKey('cms.GlossaryPage', on_delete=models.CASCADE,
                       related_name='glossary_terms')
    glossary_term = models.ForeignKey(
        'cms.GlossaryTerm', on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = "Glossary item"
        verbose_name_plural = "Glossary items"
        ordering = ['glossary_term', ]

    panels = [
        SnippetChooserPanel('glossary_term'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.glossary_term.term


class BibliographyEntryItem(models.Model):
    page = ParentalKey('cms.BibliographyPage', on_delete=models.CASCADE,
                       related_name='bibliography_entries')
    bibliography_entry = models.ForeignKey(
        'cms.BibliographyEntry',
        on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = 'Bibliography item'
        verbose_name_plural = 'Bibliography items'
        ordering = ['bibliography_entry']

    panels = [
        SnippetChooserPanel('bibliography_entry')
    ]

    def __str__(self):
        return self.page.title + " -> " + self.bibliography_entry.title


class BibliographyPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('bibliography_entries', label='Entries')
    ]


class GlossaryPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('glossary_terms', label="Terms"),
    ]
