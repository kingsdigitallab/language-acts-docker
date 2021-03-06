# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-14 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('cms', '0026_recordentrym2m'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordRankingAndFrequencyEntry',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('ranking', models.IntegerField(blank=True, null=True)),
                ('frequency', models.IntegerField(blank=True, null=True)),
                ('biblioref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cms.BiblioRef')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
