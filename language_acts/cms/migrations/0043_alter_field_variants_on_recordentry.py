# Generated by Django 2.2.7 on 2019-11-22 10:54

import language_acts.cms as cms
import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations
from wagtail.core.rich_text import RichText

field_names = [
    'collocational_history', 'diaphasic_variation', 'diatopic_variation',
    'first_attest', 'hist_freq', 'morph_related_words',
    'ranking_freq', 'semantic_history', 'variants',
]


def convert_to_streamfield(apps, schema_editor):
    for field_name in field_names:
        _convert_to_streamfield(apps, schema_editor, field_name)


def _convert_to_streamfield(apps, schema_editor, field_name):
    RecordEntry = apps.get_model('cms', 'RecordEntry')
    for page in RecordEntry.objects.all():
        field = getattr(page, field_name)

        if field.raw_text and not field:
            setattr(page, field_name, [('text', RichText(field.raw_text))])
            page.save()


def convert_to_richtext(apps, schema_editor):
    for field_name in field_names:
        _convert_to_richtext(apps, schema_editor, field_name)


def _convert_to_richtext(apps, schema_editor, field_name):
    RecordEntry = apps.get_model('cms', 'RecordEntry')
    for page in RecordEntry.objects.all():
        field = getattr(page, field_name)

        if field.raw_text is None:
            raw_text = ''.join([
                child.value.source for child in field
                if child.block_type == 'rich_text'
            ])
            setattr(page, field_name, raw_text)
            page.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('cms', '0042_alter_field_hist_freq_on_record_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordentry',
            name='collocational_history',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='diaphasic_variation',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='diatopic_variation',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='first_attest',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='hist_freq',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock(
            )), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default='', help_text='historical frequency (per million words)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='morph_related_words',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='ranking_freq',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='semantic_history',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='variants',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('html', wagtail.core.blocks.StructBlock(
                [('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML', required=False))], blank=True, default=''),
            preserve_default=False,
        ),
        migrations.RunPython(
            convert_to_streamfield,
            convert_to_richtext,
            atomic = True
        ),
    ]
