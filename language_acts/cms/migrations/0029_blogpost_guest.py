# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-14 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0028_recordentry_first_attest'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='guest',
            field=models.BooleanField(default=False, verbose_name='Guest Post'),
        ),
    ]
