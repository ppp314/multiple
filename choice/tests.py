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

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

from .models import Exam, Question

TEXTEXAMPLE = 'test one'


def create_exam(exam_author, exam_title):
    """
    Create a exam with tthe given exam_author and exam_title.
    """
    return Exam.objects.create(author=exam_author, title=exam_title)


class ExamIndexViews(TestCase):
    def test_no_exam(self):
        # If no exam exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No exam is available")
        self.assertQuerysetEqual(response.context['latest_exam_list'], [])

    def test_create_user_logged_in_user_with_no_exam(self):
        User.objects.create_user(username='ss')
        response = self.client.post(reverse('admin:login'), {'username': 'ss', 'password': ''})
        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_exam_list'], [])

    def test_create_user_logged_in_user_with_one_exam(self):
        USERNAMEEXAMPLE = 'ss'
        author = User.objects.create_user(username='ss')
        response = self.client.post(reverse('admin:login'), {'username': USERNAMEEXAMPLE, 'password': ''})
        create_exam(author, TEXTEXAMPLE)
        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_exam_list'], ['<Exam: ' + TEXTEXAMPLE + '>'])


class QuestionIndexViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ss = User.objects.create_user(username='ss')
        cls.examss = Exam.objects.create(author=cls.ss, title=TEXTEXAMPLE)

    def test_no_question(self):
        # If no question exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:question-index', kwargs={'pk': self.examss.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No question is available")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_create_user_loged_in_user_with_one_exam_and_no_question(self):
        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_exam_list'], ['<Exam: ' + TEXTEXAMPLE + '>'])

    def test_one_question(self):
        Question.objects.create(exam=self.examss, no=1, sub_no=1, point=1)
        response = self.client.get(reverse('choice:question-index', kwargs={'pk': self.examss.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['question_list'], ['<Question: 1-1>'])
        # self.assertQuerysetEqual((response.context['question_list']).exam, ['<Exam: ' + TEXTEXAMPLE + '>'])


class ExamCreateViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ss = User.objects.create_user(username='ss')
        cls.examss = Exam.objects.create(author=cls.ss, title=TEXTEXAMPLE)

    # BROKEN TEST
    # def test_create_exam(self):
    #     # First, we should know a number of Exam in the database.
    #     response = self.client.post(reverse('admin:login'), {'username': 'ss', 'password': ''})
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.get(reverse('choice:exam_index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context['latest_exam_list'], ['<Exam: ' + TEXTEXAMPLE + '>'])
    #     b = Exam.objects.count()
    #     self.assertEqual(b, 1)
    #     before = len(response.context['latest_exam_list'])
    #     self.assertEqual(before, 1)

    #     self.client.force_login(self.ss)
    #     response = self.client.post('/add/', {'title': TEXTEXAMPLE, 'author': self.ss})
    #     self.assertEqual(response.status_code, 200)

    #     response = self.client.get(reverse('choice:exam_index'))
    #     self.assertEqual(response.status_code, 200)

    #     self.assertQuerysetEqual(response.context['latest_exam_list'], ['<Exam: ' + TEXTEXAMPLE + '>'])

    #     after = len(response.context['latest_exam_list'])
    #     self.assertEqual(after, 1)
