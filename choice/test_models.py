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
from django.contrib.auth.models import User
from .models import Exam, Question, Person


# Create your tests here.
@pytest.fixture
def create_user_fixture():
    User.objects.create(
        username='fixtureuser',
        email='fixtureuser@example.com',
        password='top_secret'
    )


@pytest.mark.django_db
def test_no_exam(create_user_fixture):
    """If no question exists, count should be 0."""
    assert Exam.objects.filter(author__username='fixtureuser').count() == 0


@pytest.mark.django_db
def test_one_exam(create_user_fixture):
    """if one question exists, count should be 1."""
    user = User.objects.get(username='fixtureuser')
    Exam.objects.create(
        author=user, title="test",
        number_of_question=10,
    )
    assert Exam.objects.count() == 1


@pytest.mark.django_db
def test_no_question():
    """If no question exists, count should be 0."""
    assert Question.objects.count() == 0


@pytest.mark.django_db
def test_one_question(create_user_fixture):
    """if one question exists, count should be 1."""
    user = User.objects.get(username='fixtureuser')
    exam = Exam.objects.create(
        title='test',
        author=user,
        number_of_question=10,
    )
    Question.objects.create(
        exam=exam, no=1, sub_no=1, point=1, answer=1
    )
    assert Question.objects.count() == 1


