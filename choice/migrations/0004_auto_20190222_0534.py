# Generated by Django 2.1.7 on 2019-02-21 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0003_auto_20190220_0537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='exam',
        ),
    ]