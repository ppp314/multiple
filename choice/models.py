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
from django.db.models import Sum, F, Q
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


CHOICE_MARK_ONE = 'MARK1'
CHOICE_MARK_TWO = 'MARK2'
CHOICE_MARK_THREE = 'MARK3'
CHOICE_MARK_FOUR = 'MARK4'
CHOICE_MARK_FIVE = 'MARK5'

CHOICE_MARK_CHOICES = (
    (CHOICE_MARK_ONE, 'Mark 1'),
    (CHOICE_MARK_TWO, 'Mark 2'),
    (CHOICE_MARK_THREE, 'Mark 3'),
    (CHOICE_MARK_FOUR, 'Mark 4'),
    (CHOICE_MARK_FIVE, 'Mark 5'),
)


class CorrectAns(models.Model):
    """ The class which contains correct answers."""
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


class DrillQuerySet(models.QuerySet):
    """
    Used as a Drill class manager
    """
    def score(self):
        """Should not apply .filter() """
        mark_c = Sum(
            'mark__correctans__point',
            filter=Q(
                mark__correctans__correct_answer=F('mark__answer')
            )
        )
        return self.annotate(total_score=mark_c)


class Drill(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name='テスト名',
        max_length=200
    )

    objects = DrillQuerySet.as_manager()

    def __str__(self):
        return f"is {self.title}."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        answers = self.exam.correctans_set.all()
        for an in answers:
            Mark.objects.create(drill=self, correctans=an)

    def point_earned(self):
        p = self.exam.correctans_set.all()
        p = p.aggregate(Sum('point'))
        return p


class Mark(models.Model):
    """The class contains submitted answers."""

    drill = models.ForeignKey('Drill', on_delete=models.CASCADE)
    correctans = models.ForeignKey('CorrectAns', on_delete=models.CASCADE)
    answer = models.PositiveIntegerField(
        blank=True,
        default=100
    )

    pretty = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    def __str__(self):
        return f"is {self.answer}."
