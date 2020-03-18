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
from django.db.models import Sum, F, Q, Count
from django.urls import reverse
from django.utils import timezone


class ExamManeger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(Count('answer'),
                                               Sum('answer__point'))


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

    objects = ExamManeger()

    class Meta:

        verbose_name = '試験'
        verbose_name_plural = '試験'
        ordering = ['created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('choice:exam-detail', kwargs={'pk': self.pk})


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


class ExamManeger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(Count('answer'))


class DrillManager(models.Manager):
    """Manager used as Drill class manager."""
    def score(self):
        """Each drill queryset with a score of correct answer attribute.
        Each drill with score of the correct answer as
        a `mark_point_sum` attribute.

        Return QuerySet: the drill queryset with `total_score` attribute
        """
        pass

    def get_queryset(self):
        mark_point_sum = Sum(
            'mark__answer__point',
        )

        """

            filter=Q(
                mark__answer__correct=F('mark__your_choice')
            )
        """
        
        return super().get_queryset().annotate(
            mark_point_sum=mark_point_sum
        )


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

    objects = DrillManager()

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


class MarkManager(models.Manager):
    """Mark Manager."""
    def create_mark(self, drill, answer, your_choice=''):
        """Create mark method.
        Create and return mark object with drill and answer.
        """
        mark = self.create(
            drill=drill,
            answer=answer,
            your_choice=your_choice,
        )
        return mark


class Mark(models.Model):
    """The class contains submitted answers."""

    drill = models.ForeignKey('Drill', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    your_choice = models.CharField(
        max_length=30,
        choices=CHOICE_MARK_CHOICES,
        blank=True,
    )

    objects = MarkManager()

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


def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000

    It must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ...
    OverflowError: n too large
    """

    import math
    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result
