# Generated by Django 2.2.2 on 2019-06-23 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0051_article_publication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='author',
        ),
    ]
