# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-23 14:59
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0018_image_grid_CharBlock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='cms.EventTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
