# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-11 14:53
from __future__ import unicode_literals

import cms.models.streamfield
from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('cms', '0022_wagtail_bump'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'home', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'title', wagtail.core.blocks.CharBlock()), (b'description', wagtail.core.blocks.RichTextBlock())], icon='grip', label='Homepage Block')), (b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock(required=False)), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock()), (b'text', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Aligned image + text')), (b'grid', wagtail.core.blocks.StructBlock([(b'image_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'link', wagtail.core.blocks.URLBlock(required=False)), (b'text', wagtail.core.blocks.CharBlock(required=False))]), required=False))], icon='grip', label='Image grid')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), (b'd3', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock(required=False)), (b'css', wagtail.core.blocks.RawHTMLBlock(required=False)), (b'js', wagtail.core.blocks.RawHTMLBlock(required=False)), (b'additional_files', wagtail.core.blocks.RawHTMLBlock(required=False, verbose_name='Additional JS                                    files to load.'))], icon='media', label='D3 Visualisation')), (b'table', wagtail.contrib.table_block.blocks.TableBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]