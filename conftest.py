import pytest

from django.contrib.auth.models import User
from choice.models import Exam, CorrectAns


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
    CorrectAns.objects.create(
        exam=exam, no=1, sub_no=1, point=5, correct_answer=1
    )
    CorrectAns.objects.create(
        exam=exam, no=1, sub_no=2, point=20, correct_answer=2
    )
    CorrectAns.objects.create(
        exam=exam, no=2, sub_no=1, point=25, correct_answer=3
    )
    CorrectAns.objects.create(
        exam=exam, no=3, sub_no=1, point=25, correct_answer=4
    )
    CorrectAns.objects.create(
        exam=exam, no=4, sub_no=1, point=25, correct_answer=5
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
    CorrectAns.objects.create(
        exam=exam, no=1, sub_no=1, point=5, correct_answer=1
    )
    CorrectAns.objects.create(
        exam=exam, no=1, sub_no=2, point=20, correct_answer=2
    )
    CorrectAns.objects.create(
        exam=exam, no=2, sub_no=1, point=25, correct_answer=3
    )
    CorrectAns.objects.create(
        exam=exam, no=3, sub_no=1, point=25, correct_answer=4
    )
    CorrectAns.objects.create(
        exam=exam, no=4, sub_no=1, point=25, correct_answer=5
    )
