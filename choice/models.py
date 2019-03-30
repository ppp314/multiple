"""
Copyright 2019 Acacia Shop

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone


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

    choice1 = models.BooleanField(null=False, default=False)
    choice2 = models.BooleanField(null=False, default=False)
    choice3 = models.BooleanField(null=False, default=False)
    choice4 = models.BooleanField(null=False, default=False)
    choice5 = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'
        ordering = ['pk']

    def __str__(self):
        return str(self.no) + '-' + str(self.sub_no)
