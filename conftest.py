import pytest

from django.contrib.auth.models import User
from choice.models import Exam, Question


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
    Question.objects.create(
        exam=exam, no=1, sub_no=1, point=5, answer=1
    )
    Question.objects.create(
        exam=exam, no=1, sub_no=2, point=20, answer=2
    )
    Question.objects.create(
        exam=exam, no=2, sub_no=1, point=25, answer=3
    )
    Question.objects.create(
        exam=exam, no=3, sub_no=1, point=25, answer=4
    )
    Question.objects.create(
        exam=exam, no=4, sub_no=1, point=25, answer=5
    )

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
    Question.objects.create(
        exam=exam, no=1, sub_no=1, point=5, answer=1
    )
    Question.objects.create(
        exam=exam, no=1, sub_no=2, point=20, answer=2
    )
    Question.objects.create(
        exam=exam, no=2, sub_no=1, point=25, answer=3
    )
    Question.objects.create(
        exam=exam, no=3, sub_no=1, point=25, answer=4
    )
    Question.objects.create(
        exam=exam, no=4, sub_no=1, point=25, answer=5
    )
    

