# Generated by Django 3.0.10 on 2021-04-13 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0075_bibliography_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bibliographyentryitem',
            options={'ordering': ['bibliography_entry'], 'verbose_name': 'Bibliography item', 'verbose_name_plural': 'Bibliography items'},
        ),
        migrations.RemoveField(
            model_name='bibliographyentryitem',
            name='sort_order',
        ),
    ]
