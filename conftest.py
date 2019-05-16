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

    mkset = drill.mark_set.all()

    """
    Set answer 1 wrong answer and 19 correct answers to earn the score of 95.
    """
    mk = mkset[0]
    mk.answer = 2  # Wrong!
    mk.save()

    for mk in mkset[1:]:
        mk.answer = 1  # Correct
        mk.save()

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

    mkset = drill.mark_set.all()

    mk = mkset[0]
    mk.answer = 2
    mk.save()

    for mk in mkset[1:]:
        mk.answer = 1
        mk.save()
