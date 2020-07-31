from __future__ import unicode_literals
from __future__ import unicode_literals

import logging
from datetime import date

# from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import QuerySet
from django.shortcuts import render
from django.utils.text import slugify
from haystack.query import SearchQuerySet
from kdl_wagtail.core.models import IndexPage
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from .behaviours import WithFeedImage, WithStreamField
from .streamfield import RecordEntryStreamBlock, CMSStreamBlock

logger = logging.getLogger(__name__)


def _paginate(request, items):
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        items = paginator.page(1)

    return items


# class IndexPage(Page, WithStreamField):
#     search_fields = Page.search_fields + [
#         index.SearchField('body'),
#     ]
#     strands = ParentalManyToManyField('cms.StrandPage', blank=True)
#     subpage_types = ['IndexPage', 'RichTextPage']
#
#
# IndexPage.content_panels = [
#     FieldPanel('title', classname='full title'),
#     StreamFieldPanel('body'),
# ]
#
# IndexPage.promote_panels = Page.promote_panels


class StrandPage(IndexPage, WithStreamField):
    blogs_contextual_information = RichTextField(blank=True, null=True)
    events_contextual_information = RichTextField(blank=True, null=True)
    news_contextual_information = RichTextField(blank=True, null=True)

    subpage_types = ['kdl_wagtail_core.IndexPage',
                     'kdl_wagtail_core.RichTextPage',
                     'RecordIndexPage']

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    def show_filtered_content(self):
        return True

    def get_context(self, request, *args, **kwargs):
        context = super(StrandPage, self).get_context(request)

        context['blog_posts'] = BlogPost.get_by_strand(
            self.title)
        # todo ADD!
        # context['events'] = Event.get_by_strand(
        #     self.title)
        # context['past_events'] = Event.get_past_by_strand(
        #     self.title)
        # context['news_posts'] = NewsPost.get_by_strand(
        #     self.title)

        return context


StrandPage.content_panels = [
    FieldPanel('blogs_contextual_information'),
    FieldPanel('events_contextual_information'),
    FieldPanel('news_contextual_information'),
]


class RecordIndexPage(Page):
    search_fields = Page.search_fields + [
    ]

    subpage_types = ['RecordPage']

    def get_context(self, request, *args, **kwargs):
        context = super(RecordIndexPage, self).get_context(request)

        # Get selected facets
        selected_facets = set(request.GET.getlist('selected_facets'))

        # Init a search query set
        sqs = SearchQuerySet().models(RecordPage)

        # Apply currently selected facets
        for facet in selected_facets:
            sqs = sqs.narrow(facet)

        # Get facet counts
        sqs = sqs.facet('language').facet('word_type').facet('first_letter')

        # Generate presentable facet data
        selected_facets_ui = []

        for facet in selected_facets:
            f = {
                'value': facet.split(':')[1],
                'remove_url': request.get_full_path().replace(
                    '&selected_facets={}'.format(facet), '')
            }
            selected_facets_ui.append(f)

        context['selected_facets'] = selected_facets_ui
        context['sqs'] = sqs

        return context


RecordIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
]

RecordIndexPage.promote_panels = Page.promote_panels


class RecordPage(Page):
    latin_lemma = RichTextField(blank=True, null=True)

    latin_pos = ParentalManyToManyField('cms.POSLabel', blank=True)

    latin_meaning = RichTextField(blank=True, null=True)

    cultural_transmission = StreamField(
        CMSStreamBlock(required=False, blank=True))

    search_fields = Page.search_fields + [
    ]

    subpage_types = ['RecordEntry']

    def get_languages(self):
        return RecordEntry.objects.live().descendant_of(self).order_by(
            'language__order_by')


RecordPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('latin_lemma'),
    FieldPanel('latin_pos', widget=forms.CheckboxSelectMultiple),
    FieldPanel('latin_meaning'),
    StreamFieldPanel('cultural_transmission')
]

RecordPage.promote_panels = Page.promote_panels


class RecordEntry(Page):
    language = models.ForeignKey(
        'cms.LemmaLanguage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    lemma = models.CharField(
        max_length=2048, blank=True, null=True)

    variants = StreamField(RecordEntryStreamBlock, blank=True)

    pos = ParentalManyToManyField('cms.POSLabel', blank=True)

    morph_related_words = StreamField(RecordEntryStreamBlock, blank=True)
    ranking_freq = StreamField(RecordEntryStreamBlock, blank=True)
    first_attest = StreamField(RecordEntryStreamBlock, blank=True)
    hist_freq = StreamField(RecordEntryStreamBlock, blank=True,
                            verbose_name='Historical frequency')
    hist_freq_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='[OR] Pre-rendered Graph Image',
        help_text='Pre-rendered graph will take priority over manual data\
            inputted above.'
    )
    semantic_history = StreamField(RecordEntryStreamBlock, blank=True)
    collocational_history = StreamField(RecordEntryStreamBlock, blank=True)
    diatopic_variation = StreamField(RecordEntryStreamBlock, blank=True)
    diaphasic_variation = StreamField(RecordEntryStreamBlock, blank=True)

    search_fields = Page.search_fields + [
    ]

    subpage_types = []

    @property
    def url(self):
        return self.get_parent().url


RecordEntry.content_panels = [
    FieldPanel('title', classname='full title'),
    SnippetChooserPanel('language'),
    FieldPanel('lemma'),
    StreamFieldPanel('variants'),
    FieldPanel('pos', widget=forms.CheckboxSelectMultiple),
    StreamFieldPanel('morph_related_words'),
    StreamFieldPanel('ranking_freq'),
    StreamFieldPanel('first_attest'),
    MultiFieldPanel(
        [
            StreamFieldPanel('hist_freq'),
            ImageChooserPanel('hist_freq_image')
        ],
        heading='Historical Frequency (per million words)',
        classname="collapsible collapsed"
    ),
    StreamFieldPanel('semantic_history'),
    StreamFieldPanel('collocational_history'),
    StreamFieldPanel('diatopic_variation'),
    StreamFieldPanel('diaphasic_variation'),
]


@register_snippet
class BlogAuthor(models.Model):
    author_name = models.CharField(max_length=512, default='')
    first_name = models.CharField(max_length=512, default='')
    last_name = models.CharField(max_length=512, default='')
    author_slug = models.CharField(max_length=512, default='')

    def save(self, *args, **kwargs):
        # update author slug
        self.author_slug = slugify(self.author_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.author_name


class BlogIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        today = date.today()
        posts = BlogPost.objects.live().descendant_of(
            self).filter(date__lte=today)

        posts = posts.order_by('-date')

        return posts

    @route(r'^$')
    def all_posts(self, request):
        posts = self.posts

        return render(request, self.get_template(request),
                      {'self': self, 'posts': _paginate(request, posts)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )

    def get_author(self, author_slug: str) -> QuerySet:
        if author_slug:
            return self.posts.filter(
                author__author_slug=author_slug
            )
        return BlogAuthor.objects.none()

    @route(r'^author/(?P<author>[\w\- ]*)/$')
    def author(self, request, author=None):
        posts = self.get_author(author)
        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'author', 'filter': author
            }
        )


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPost',
        on_delete=models.CASCADE, related_name='tagged_items')

    @property
    def name(self):
        """This has been added because of an error in
        _edit_string_for_tags(tags) in taggit getting the parent object
        not the tag, and failing with an Attribute Error. May need to be
        revisited"""
        if self.tag:
            return self.tag.name
        return ''


class BlogPost(Page, WithStreamField, WithFeedImage):
    date = models.DateField()
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    strands = ParentalManyToManyField('cms.StrandPage', blank=True)
    guest = models.BooleanField(default=False,
                                verbose_name="Guest Post",
                                help_text='Create new guest author in snippets'
                                )
    author = models.ForeignKey('BlogAuthor',
                               verbose_name="Author",
                               blank=True, null=True,
                               on_delete=models.SET_NULL,
                               help_text=("select guest author or leave blank"
                                          " for default user")
                               )
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('date'),
        index.SearchField('author'),
        index.RelatedFields('tags', [
            index.SearchField('name'),
            index.SearchField('slug'),
        ]),
    ]

    subpage_types = []

    def get_index_page(self):
        # Find closest ancestor which is a blog index
        return BlogIndexPage.objects.ancestor_of(self).last()

    def save(self, *args, **kwargs):
        if not self.author:
            # set the author to either the current user
            # or if guest is checked, the generic guest author
            if self.guest:
                try:
                    self.author = BlogAuthor.objects.get(author_name='guest')
                except ObjectDoesNotExist:
                    logger.error("Generic Guest Author does not exist!")
                    return
            else:
                try:
                    self.author = BlogAuthor.objects.get(
                        author_name=self.owner.username
                    )
                except ObjectDoesNotExist:
                    # Author for this user does not exist, create one
                    author, created = BlogAuthor.objects.get_or_create(
                        author_name=self.owner.username,
                        first_name=self.owner.first_name,
                        last_name=self.owner.last_name,
                    )
                    self.author = author

        super().save(*args, **kwargs)

    @classmethod
    def get_by_tag(cls, tag=None):
        today = date.today()
        if tag:
            return cls.objects.live().filter(
                tags__name=tag).filter(date__lte=today).order_by('-date')
        else:
            return cls.objects.none()

    @classmethod
    def get_by_author(cls, author=None):
        if author:
            return cls.objects.live().filter(author__author_name=author)
        return cls.objects.none()

    @classmethod
    def get_by_strand(cls, strand_name=None):
        today = date.today()
        if strand_name:
            try:
                strand = StrandPage.objects.get(title=strand_name)
                return cls.objects.live().filter(
                    strands=strand).filter(date__lte=today).order_by('-date')
            except ObjectDoesNotExist:
                return cls.objects.none()
        else:
            return cls.objects.none()


BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    MultiFieldPanel([
        FieldPanel('guest'),
        FieldPanel('author'),
    ]),
    StreamFieldPanel('body'),
]

BlogPost.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
    ImageChooserPanel('feed_image'),
    FieldPanel('strands', widget=forms.CheckboxSelectMultiple),
]

BlogPost.settings_panels = Page.settings_panels + [
    FieldPanel('owner'),
]

# class RichTextPage(Page, WithStreamField):
#     search_fields = Page.search_fields + [
#         index.SearchField('body'),
#     ]
#
#     subpage_types = []
#
#
# RichTextPage.content_panels = [
#     FieldPanel('title', classname='full title'),
#     StreamFieldPanel('body'),
# ]
#
# RichTextPage.promote_panels = Page.promote_panels
