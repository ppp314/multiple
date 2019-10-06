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

from django.utils import timezone
from django.contrib.auth.models import User
from choice.models import Exam, Answer, Drill,\
    CHOICE_MARK_ONE,\
    CHOICE_MARK_TWO
from choice.models import Publication, Article


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
        number_of_question=10,
    )

    for i in range(1, 21):
        Answer.objects.create(
            exam=exam, no=i, sub_no=1, point=5,
            correct=CHOICE_MARK_ONE
        )

    drill = Drill.objects.create(
        exam=exam,
        description="Test Drill one",
        created=timezone.now(),
    )

    mkset = (
        drill
        .mark_set.
        order_by(
            'answer__no',
            'answer__sub_no'
        )
    )

    """
    Set answer 1 wrong answer and 19 correct answers to earn the score of 95.
    """
    mk = mkset[0]
    mk.your_choice = CHOICE_MARK_TWO  # Wrong!
    mk.save()
    for mk in mkset[1:]:
        mk.your_choice = CHOICE_MARK_ONE  # Correct
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
        number_of_question=10,
    )

    for i in range(1, 21):
        Answer.objects.create(
            exam=exam, no=i, sub_no=1, point=5,
            correct=CHOICE_MARK_ONE
        )

    drill = Drill.objects.create(
        exam=exam,
        description="Test Drill one",
        created=timezone.now(),
    )

    mkset = (
        drill
        .mark_set.
        order_by(
            'answer__no',
            'answer__sub_no'
        )
    )

    mk = mkset[0]
    mk.your_choice = CHOICE_MARK_TWO  # Wrong!
    mk.save()
    for mk in mkset[1:]:
        mk.your_choice = CHOICE_MARK_ONE  # Correct
        mk.save()


@pytest.fixture
def create_publication():
    """
    The first fixture
    """
    Publication.objects.create(
        title="Journal Standard"
    )
