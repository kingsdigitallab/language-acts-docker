# Generated by Django 2.2.6 on 2019-10-29 12:48

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0039_rename_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordentry',
            name='diaphasic_variation',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='diatopic_variation',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='first_attest',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='hist_freq',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='morph_related_words',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='ranking_freq',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='variants',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordpage',
            name='latin_lemma',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recordpage',
            name='latin_meaning',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
