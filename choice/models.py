'''
Copyright 2019 Acacia Shop

This file is part of multiple.

    Multiple is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Multiple is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    Along with multiple.  If not, see <https://www.gnu.org/licenses/>.
'''

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.forms.formsets import formset_factory, BaseFormSet
from django import forms


class Exam(models.Model):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    title = models.CharField(
        verbose_name='テスト名',
        max_length=200
        )

    created_date = models.DateTimeField(
        verbose_name='作成日',
        default=timezone.now
        )

    number_of_question = models.IntegerField(
        verbose_name='問題数',
        default=1
        )

    class Meta:

        verbose_name = '試験'
        verbose_name_plural = '試験'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('choice:question-index', kwargs={'pk': self.pk})


class Question(models.Model):

    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

    no = models.IntegerField(
        verbose_name='大問',
        default=0
        )

    sub_no = models.IntegerField(
        verbose_name='小問',
        default=0
        )

    point = models.IntegerField(
        verbose_name='配点',
        default=0
        )

    correct_answer = models.PositiveIntegerField(
        verbose_name='正解',
        default=1
        )

    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'
        ordering = ['pk']

    def __str__(self):
        return str(self.no) + '-' + str(self.sub_no)


class Drill(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name='テスト名',
        max_length=200
        )


class Answer(models.Model):
    drill = models.ForeignKey('Drill', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.PositiveIntegerField(
        default=1
        )
