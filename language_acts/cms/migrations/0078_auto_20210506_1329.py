# Generated by Django 3.0.10 on 2021-05-06 13:29

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0077_glossary_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryterm',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='glossaryterm',
            name='term',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
