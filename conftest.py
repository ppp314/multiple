import pytest

from django.contrib.auth.models import User
from choice.models import Exam, CorrectAns, Drill


@pytest.fixture
def create_user_exam_fixture():
    """
    The first fixture
    """
    user = User.objects.create(
        username='dokinchan',
        email='docinchan@example.com',
        password='top_secret'
    )
    exam = Exam.objects.create(
        title='test1',
        author=user,
        number_of_question=10,
    )

    for i in range(1, 21):
        CorrectAns.objects.create(
            exam=exam, no=i, sub_no=1, point=5, correct_answer=1
        )

    drill = Drill.objects.create(
        exam=exam,
        title="Test Drill one"
    )

    anset = drill.answer_set.all()

    """
    Set answer 1 wrong answer and 19 correct answers to earn the score of 95.
    """
    an = anset[0]
    an.answer = 2  # Wrong!
    an.save()

    for an in anset[1:]:
        an.answer = 1  # Correct
        an.save()

    """
    The second fixture
    """
    user = User.objects.create(
        username='baikinman',
        email='baikinman@example.com',
        password='top_secret'
    )
    exam = Exam.objects.create(
        title='test2',
        author=user,
        number_of_question=10,
    )

    for i in range(1, 21):
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
    an.save()

    for an in anset[1:]:
        an.answer = 1
        an.save()
