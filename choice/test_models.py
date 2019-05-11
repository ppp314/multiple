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
from .models import Exam, CorrectAns
from .models import Drill

pytestmark = pytest.mark.django_db


# Create your tests here.
def test_one_exam(create_user_exam_fixture):
    """Test if no question exists. The count should be 0."""
    assert Exam.objects.filter(author__username='dokinchan').count() == 1


def test_no_question():
    """Test if no question exists, count should be 0."""
    assert CorrectAns.objects.count() == 0


def test_two_exam(create_user_exam_fixture):
    """Test if there are two questions existing. The count should be 2."""
    assert Exam.objects.count() == 2


def test_one_drill(create_user_exam_fixture):
    """
    Test if one drill and the same number of
    answer can be made.
    """
    e = Exam.objects.first()
    d = Drill(title="Test")
    d.exam = e
    d.save()
    assert d.answer_set.count() == e.correctans_set.count()
