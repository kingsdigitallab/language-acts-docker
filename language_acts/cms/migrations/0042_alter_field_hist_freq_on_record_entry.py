# Generated by Django 2.2.7 on 2019-11-22 10:09

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0041_auto_20191118_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordentry',
            name='hist_freq',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='historical frequency (per million words)', null=True),
        ),
    ]
