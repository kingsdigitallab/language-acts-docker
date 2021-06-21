# Generated by Django 3.0.10 on 2021-05-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0080_glossarytermitem_ordering'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossarytermitem',
            options={'ordering': ['term_raw'], 'verbose_name': 'Glossary item', 'verbose_name_plural': 'Glossary items'},
        ),
        migrations.AddField(
            model_name='glossarytermitem',
            name='term_raw',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]