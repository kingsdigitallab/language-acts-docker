# Generated by Django 2.2.10 on 2020-10-14 13:47

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wagtailcore',
         '0041_group_collection_permissions_verbose_name_plural'),
        ('cms', '0065_glossarypage_glossarytermitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibliographyPage',
            fields=[
                ('page_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BibliographyEntryItem',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('sort_order',
                 models.IntegerField(blank=True, editable=False, null=True)),
                ('bibliography_entry', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+', to='cms.BibliographyEntry')),
                ('page', modelcluster.fields.ParentalKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='bibliography_entries',
                    to='cms.BibliographyPage')),
            ],
            options={
                'verbose_name': 'Bibliography item',
                'verbose_name_plural': 'Bibliography items',
            },
        ),
    ]
