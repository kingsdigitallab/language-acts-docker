# Generated by Django 2.2.13 on 2020-06-25 14:05

from django.contrib.auth.models import User
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0054_blog_author'),
    ]

    def add_blog_authors(apps, schema_editor):
        BlogAuthor = apps.get_model('cms', 'BlogAuthor')
        BlogPost = apps.get_model('cms', 'BlogPost')
        # Add all current users as authors username first_name last_name
        for user in User.objects.all():
            author, created = BlogAuthor.objects.get_or_create(
                author_name=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            for post in BlogPost.objects.filter(owner__pk=user.pk):
                post.author = author
                print("{}:{}\n".format(author.author_name, post))
                post.save()

    operations = [
        migrations.RunPython(add_blog_authors),
    ]
