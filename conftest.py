import pytest

from django.contrib.auth.models import User
from choice.models import Exam, CorrectAns, Drill


@pytest.fixture
def create_user_exam_fixture():
    user = User.objects.create(
        username='dokinchan',
        email='docinchan@example.com',
        password='top_secret'
    )
    exam = Exam.objects.create(
        title='test',
        author=user,
        number_of_question=10,
    )

    for i in range(1, 20):
        CorrectAns.objects.create(
            exam=exam, no=i, sub_no=1, point=5, correct_answer=1
        )

    drill = Drill.objects.create(
        exam=exam,
        title="Test Drill one"
    )

    anset = drill.answer_set.all()

    an = anset[0]
    an.answer = 2

    for an in anset[1:]:
        an.answer = 1
    an.save()

    user = User.objects.create(
        username='baikinman',
        email='baikinman@example.com',
        password='top_secret'
    )
    exam = Exam.objects.create(
        title='test',
        author=user,
        number_of_question=10,
    )

    for i in range(1, 20):
        CorrectAns.objects.create(
            exam=exam, no=i, sub_no=1, point=5, correct_answer=1
        )

    drill = Drill.objects.create(
        exam=exam,
        title="Test Drill one"
    )

    anset = drill.answer_set.all()

    an = anset[0]
    an.answer = 2

    for an in anset[1:]:
        an.answer = 1
    an.save()
