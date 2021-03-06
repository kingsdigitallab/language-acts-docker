# Generated by Django 2.2.13 on 2020-06-24 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0050_guest_blank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='guest_author',
            field=models.ForeignKey(
                blank=True,
                help_text='Create new author in snippets',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='cms.BlogGuestAuthor',
                verbose_name='Guest post author'),
        ),
    ]
