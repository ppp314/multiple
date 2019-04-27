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

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Exam, Question

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


class FormSetCreateViewTest(TestCase):
    """ Test if FormSet Create view contains the management form piece."""

   
class ExamQuestionInlineViewTest(TestCase):
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


class HomeViewTest(TestCase):
    """ Test if teh page Home is available"""
    def test_get_home_view(self):
        url = reverse('choice:home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'choice/home.html')
        self.assertTemplateUsed(response, 'choice/base.html')
        self.assertEqual(response.status_code, 200)


class AboutViewTest(TestCase):
    """ Test if teh page about is available"""
    def test_get_home_view(self):
        url = reverse('choice:about')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'choice/about.html')
        self.assertTemplateUsed(response, 'choice/base.html')
        self.assertEqual(response.status_code, 200)


class ExamListViews(TestCase):
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
