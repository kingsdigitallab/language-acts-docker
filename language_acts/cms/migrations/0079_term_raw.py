# Generated by Django 3.0.10 on 2021-05-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0078_auto_20210506_1329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossaryterm',
            options={'ordering': ['term_raw'], 'verbose_name': 'Glossary term', 'verbose_name_plural': 'Glossary terms'},
        ),
        migrations.AddField(
            model_name='glossaryterm',
            name='term_raw',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
