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
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Exam, Question
from .views import PersonCarCreateFormsetView
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

   
class TestExamQuestionInlineView(TestCase):
    """
        Test inlineformset_factory.
    """
    def test_get_exam_quesion_inline(self):
        """ Test method==GET"""
        url = reverse('choice:add-question')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'question_set-TOTAL_FORMS')
        self.assertContains(response, 'question_set-INITIAL_FORMS')
        self.assertContains(response, 'question_set-MIN_NUM_FORMS')
        self.assertContains(response, 'question_set-MAX_NUM_FORMS')

    def test_post_exam_question_inline(self):
        """ Test method==POST"""
        author = User.objects.get_or_create(username='ss')[0]

        data = {'author': author,
                'Title': "TESTURL",
                'question_set-TOTAL_FORMS': "5",
                'question_set-INITIAL_FORMS': "0",
                'question_set-MIN_NUM_FORMS': "0",
                'question_set-MAX_NUM_FORMS': "5"
                }
        url = reverse('choice:add-question')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


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


class TestExamListViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@example.com',
            password='top_secret')

    def test_no_exam_and_one_exam(self):
        # If no exam exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:exam-list'))
        self.assertTemplateUsed(response, 'choice/exam_list.html')
        self.assertTemplateUsed(response, 'choice/base.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_exam_list']), 0)
        self.assertContains(response, "No exam is available")

        self.exam = Exam.objects.create(
            author=self.user, title='Test',
            number_of_question=1)
        response = self.client.get(reverse('choice:exam-list'))
        self.assertTemplateUsed(response, 'choice/exam_list.html')
        self.assertTemplateUsed(response, 'choice/base.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_exam_list']), 1)


        def test_create_user_logged_in_user_with_no_exam(self):
        #    User.objects.create_user(username='ss')
        #    Login as 'ss' without password
            response = self.client.get(reverse('choice:exam-list'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['latest_exam_list']), 0)

        def test_create_user_logged_in_user_with_add_one_exam(self):
            Uauthor = User.objects.get(username='ss')
            create_exam(Uauthor, "Test exam")

            response = self.client.get(reverse('choice:exam-list'))
            self.assertEqual(len(response.context['latest_exam_list']), 1)
            self.assertContains(response, "Test exam")


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
