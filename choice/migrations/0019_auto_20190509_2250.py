# Generated by Django 2.1.7 on 2019-05-09 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0018_auto_20190509_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='quesion',
            new_name='question',
        ),
    ]