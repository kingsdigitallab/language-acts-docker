# Generated by Django 3.0.10 on 2020-11-09 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0068_bibliography_surname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bibliographyentry',
            old_name='author_firstame',
            new_name='author_firstname',
        ),
    ]
