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


from django.test import TestCase, Client
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


class ExamIndexViewsNoExam(TestCase):
    def test_no_exam(self):
        ''' If no exam exists, an approperiate messages is to be displayed '''
        response = self.client.get(reverse('choice:exam-index'))
        self.assertContains(response, "No exam is available")
        self.assertQuerysetEqual(response.context['latest_exam_list'], [])


class ExamIndexViews(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        author = User.objects.get_or_create(username='ss')[0]
        self.client.force_login(author)

    def test_no_exam(self):
        # If no exam exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_exam_list']), 5)

    def test_create_user_logged_in_user_with_no_exam(self):
        #    User.objects.create_user(username='ss')
        #    Login as 'ss' without password

        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_exam_list']), 5)

    def test_create_user_logged_in_user_with_add_one_exam(self):
        Uauthor = User.objects.get(username='ss')
        create_exam(Uauthor, "Test exam")
        response = self.client.get(reverse('choice:exam-index'))

        self.assertEqual(len(response.context['latest_exam_list']), 6)
        self.assertContains(response, "Test exam")


class ExamDetailViews(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        author = User.objects.get_or_create(username='ss')[0]
        self.client.force_login(author)

    def test_exam_detail_view_not_found(self):
        url = reverse('choice:exam-detail', args=(2,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_exam_detail_view(self):
        test_pk = 1
        url = reverse('choice:exam-detail', args=(test_pk,))
        response = self.client.get(url)
        self.assertNotEqual(response.context['exam_detail'], [])

        # Test if the view contains the links to the delete page, the index page and the update page
        self.assertContains(response, reverse('choice:exam-delete', args=(test_pk,)))
        self.assertContains(response, reverse('choice:exam-update', args=(test_pk,)))
        self.assertContains(response, reverse('choice:exam-index'))
        self.assertTemplateUsed(response, 'choice/detail.html')


class QuestionIndexViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ss = User.objects.create_user(username='ss')
        cls.examss = Exam.objects.create(author=cls.ss, title=TEXTEXAMPLE)

    def test_no_question(self):
        # If no question exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:question-index', kwargs={'pk': self.examss.id}))
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

    
