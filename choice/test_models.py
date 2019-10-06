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
