# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-10 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0025_loaded_meanings_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordEntryM2M',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cms.RecordEntry')),
                ('source', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='morph_words_relationship', to='cms.RecordEntry')),
            ],
        ),
    ]
