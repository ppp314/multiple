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
import pdb
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Exam, Question
from .views import PersonCarCreateFormsetView, \
    PersonQuestionCreateFromSetView
from .forms import MyExamForm

"""
    Page URL name temmplate
    Home  /      'home'    choice/home.html
    About /about 'about'   choice/about.html
    Help  /help  'help'    choice/help.html
    Login /login 'login'
    Index /list/  'exam-list'  choice/exam-list.html
    DetailExam /detail/<int:pk> 'exam-detail'
    UpdateExam /update/<int:pk> 'exam-update'
    DeleteExam /delete/<int:pk> 'exam-delete'
    CreateExam /create/<int:pk> 'exam-create'
"""


class TestFormSetCreateView(TestCase):
    """ Test if FormSet Create view contains the management form piece."""
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_url,expected_template", [
        ("choice:about",
         ["choice/about.html", "choice/base.html"]),
        ("choice:home",
         ["choice/home.html", "choice/base.html"]),
        ("choice:exam-create",
         ["choice/exam_form.html", "choice/base.html"]),
        ("choice:success",
         ["choice/success.html", "choice/base.html"]),
        ("choice:exam-ppp",
         ["choice/person_formset.html", "choice/base.html"]),
    ],)
def test_get_simple_view(client, test_url, expected_template):
    """ Test if the page about is available"""
    url = reverse(test_url)
    response = client.get(url)
    for e in expected_template:
        assert e in [t.name for t in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_exam_by_post():
    assert Exam.objects.count() == 0
    test_author = User.objects.create_user(
        username='jacob',
        email='jacob@example.com',
        password='top_secret')

    form_data = {'title': "Test One",
                 'author': test_author.id,
                 'created_date': timezone.now(),
                 'number_of_question': 10,
                 'q_tobemade': 15, }

    form = MyExamForm(data=form_data)
    print(form.errors)
    assert form.is_valid()


def test_many_formset_view(client):
    form = PersonCarCreateFormsetView(
        factory_kwargs={'extra': 30}
        )
    print(form.inlines)


def test_person_question_view():
    factory = RequestFactory()
    request = factory.get(reverse("choice:exam-create2"))
    response = PersonQuestionCreateFromSetView.as_view()(request)
    assert response.status_code == 200
