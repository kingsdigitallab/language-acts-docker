# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_event_time_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_to',
            field=models.DateField(blank=True, null=True, verbose_name='End Date (Leave blank if not required)'),
        ),
    ]