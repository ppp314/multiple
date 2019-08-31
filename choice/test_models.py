"""
Copyright 2019 Acacia Shop

This file is part of Multiple.

    Multiple is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Multiple is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Multiple.  If not, see <https://www.gnu.org/licenses/>.
"""

import pytest
from .models import Exam, Answer
from .models import Drill, Grade
from django.utils import timezone
from django.db.models import Sum, F
from django.db import transaction


pytestmark = pytest.mark.django_db


# Create your tests here.
def test_one_exam(create_user_exam_fixture):
    """Test if no question exists. The count should be 0."""
    assert Exam.objects.count() == 2


def test_no_question():
    """Test if no question exists, count should be 0."""
    assert Answer.objects.count() == 0


def test_two_exam(create_user_exam_fixture):
    """Test if there are two questions existing. The count should be 2."""
    assert Exam.objects.count() == 2


def test_one_drill(create_user_exam_fixture):
    """
    Test if one drill and the same number of
    answer can be made.
    Answer.save() is configured properly.
    """
    e = Exam.objects.first()
    d = Drill(
        description="Test",
        created=timezone.now()
    )
    d.exam = e
    d.save()
    assert d.mark_set.count() == e.answer_set.count()


def test_point(create_user_exam_fixture):
    """Test if each point is properly set."""
    assert Answer.objects.count() == 40
    assert Answer.objects.all().aggregate(
        Sum('point')
    )['point__sum'] == 200


def test_point_one_user(create_user_exam_fixture):
    """
    Test total point.
    There are the one wrong answer and the nineteen correct answers,
    which are 5 points each.
    """
    ex = Exam.objects.first()
    d = Drill.objects.filter(exam=ex)[0]
    an = d.mark_set.all().order_by(
        'answer__no',
        'answer__sub_no',
    )
    assert an.filter(
        your_choice=F('answer__correct')
    ).aggregate(
        Sum('answer__point')
    )['answer__point__sum'] == 95


def test_drill_annotation(create_user_exam_fixture):
    """
    Test drill point
    """
    exam = Exam.objects.get(title="test1")
    thisdrill = Drill.objects.get(exam=exam)

    assert thisdrill.point_full_mark()['total'] == 100
    assert thisdrill.point_earned()['total'] == 95


def test_should_create_grade_object(create_user_exam_fixture):
    """
    Test if can create grade object.
    """
    exam = Exam.objects.get(title="test1")
    point = Drill.objects.filter(exam=exam).score()[0].total_score

    asof = timezone.now()

    before = Grade.objects.count()
    Grade.objects.create(
        exam=exam,
        point=point,
        created=asof,
    )
    after = Grade.objects.count()

    assert before + 1 == after

    before = after
    thisdrill = Drill.objects.get(exam=exam)
    thisdrill.register_grade()
    after = Grade.objects.count()

    assert before + 1 == after
