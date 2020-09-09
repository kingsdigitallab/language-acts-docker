# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-17 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0029_blogpost_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordentry',
            name='first_attest_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='First Attestation Year'),
        ),
        migrations.AlterField(
            model_name='recordentry',
            name='first_attest',
            field=models.TextField(blank=True, null=True, verbose_name='First Attestation Text'),
        ),
    ]
