# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 11:43
from __future__ import unicode_literals

import language_acts.cms as cms
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='RichTextPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
