# Generated by Django 2.1.7 on 2019-05-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0032_remove_mark_pretty'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='pretty',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
