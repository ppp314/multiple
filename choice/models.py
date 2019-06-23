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

    title = models.CharField(
        verbose_name='テスト名',
        max_length=200
    )

    created = models.DateTimeField(
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
        return reverse('choice:exam-detail', args=(self.pk,))


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


class Answer(models.Model):
    """ The class which contains correct answers."""
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

    created = models.DateTimeField(
        verbose_name='作成日',
        blank=True,
        default=None,
        null=True
    )

    no = models.IntegerField(
        verbose_name='大問',
        default=0
    )

    sub_no = models.PositiveIntegerField(
        verbose_name='小問',
        default=0
    )

    point = models.PositiveIntegerField(
        verbose_name='配点',
        default=0
    )

    correct = models.CharField(
        max_length=30,
        choices=CHOICE_MARK_CHOICES,
        blank=True,
    )

    class Meta:
        verbose_name = '解答'
        verbose_name_plural = '解答'
        ordering = ['no', 'sub_no']

    def __str__(self):
        return str(self.no) + '-' + str(self.sub_no)


class DrillQuerySet(models.QuerySet):
    """Manager used as Drill class manager."""
    def score(self):
        """Each drill queryset with a score of correct answer attribute.

        Each drill with score of the correct answer as
        a `total_score` attribute.

        Returns:
            QuerySet: the drill queryset with `total_score` attribute

        Should not apply .filter() in this function.
        """
        mark_c = Sum(
            'mark__answer__point',
            filter=Q(
                mark__answer__correct=F('mark__your_choice')
            )
        )
        return self.annotate(total_score=mark_c)


class Drill(models.Model):
    """Hold Drill object for the Exam instance."""

    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

    description = models.CharField(
        verbose_name='ドリルの説明',
        max_length=200
    )

    created = models.DateTimeField(
        verbose_name='作成日',
        blank=True,
        default=None,
        null=True
    )

    objects = DrillQuerySet.as_manager()

    def __str__(self):
        return f"is {self.description}."

    def save(self, *args, **kwargs):
        """Save the drill instance as well as create the Mark objects.

        Create the Mark objects as many as the answer objects.
        Todo:
            Work around when there is no answer object.
        """

        super().save(*args, **kwargs)
        answers = self.exam.answer_set.all()
        for an in answers:
            Mark.objects.create(drill=self, answer=an)

    def point_full_mark(self):
        """ Return the dictionary of the sum of the allocated point.

        Returns:
            the dictionary of total: {'total': 100}
        """
        p = self.exam.answer_set.all()
        dict = p.aggregate(
            total=Sum('point')
        )
        return dict  # {'total': 100}

    def point_earned(self):
        """ Return the sum of point earned."""
        qs = Mark.objects.filter(drill=self)

        dict = qs.aggregate(
            total=Sum(
                'answer__point',
                filter=Q(
                    answer__correct=F('your_choice')
                )
            )
        )
        return dict  # {'total': 100}

    def register_grade(self):
        """Register the result of this drill."""
        dict = self.point_earned()
        Grade.objects.create(
            exam=self.exam,
            point=dict['total'],
            created=timezone.now(),
        )


class Mark(models.Model):
    """The class contains submitted answers."""

    drill = models.ForeignKey('Drill', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    your_choice = models.CharField(
        max_length=30,
        choices=CHOICE_MARK_CHOICES,
        blank=True,
    )

    def __str__(self):
        return f"is {self.your_choice}."


class Grade(models.Model):
    """Hold the results of drills.

    """
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    point = models.PositiveIntegerField(
        blank=True
    )
    created = models.DateTimeField(
        blank=True,
        default=None,
    )

    def __str__(self):
        return f"is {self.point}"


class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ('headline',)

    def __str__(self):
        return self.headline    
