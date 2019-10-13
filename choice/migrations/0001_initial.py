# Generated by Django 2.2.5 on 2019-10-12 09:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=None, null=True, verbose_name='作成日')),
                ('no', models.IntegerField(default=0, verbose_name='大問')),
                ('sub_no', models.PositiveIntegerField(default=0, verbose_name='小問')),
                ('point', models.PositiveIntegerField(default=0, verbose_name='配点')),
                ('correct', models.CharField(blank=True, choices=[('MARK1', 'Mark 1'), ('MARK2', 'Mark 2'), ('MARK3', 'Mark 3'), ('MARK4', 'Mark 4'), ('MARK5', 'Mark 5')], max_length=30)),
            ],
            options={
                'verbose_name': '解答',
                'verbose_name_plural': '解答',
                'ordering': ['no', 'sub_no'],
            },
        ),
        migrations.CreateModel(
            name='Drill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='ドリルの説明')),
                ('created', models.DateTimeField(blank=True, default=None, null=True, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='テスト名')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('number_of_question', models.IntegerField(default=1, verbose_name='問題数')),
            ],
            options={
                'verbose_name': '試験',
                'verbose_name_plural': '試験',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_choice', models.CharField(blank=True, choices=[('MARK1', 'Mark 1'), ('MARK2', 'Mark 2'), ('MARK3', 'Mark 3'), ('MARK4', 'Mark 4'), ('MARK5', 'Mark 5')], max_length=30)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choice.Answer')),
                ('drill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choice.Drill')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.PositiveIntegerField(blank=True)),
                ('created', models.DateTimeField(blank=True, default=None)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choice.Exam')),
            ],
        ),
        migrations.AddField(
            model_name='drill',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choice.Exam'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=100)),
                ('publications', models.ManyToManyField(to='choice.Publication')),
            ],
            options={
                'ordering': ('headline',),
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choice.Exam'),
        ),
    ]
