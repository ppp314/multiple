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


from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
import unittest


# Create your tests here.

from .models import Exam, Question, BookmarkFormSet, QuestionFormSet
from .views import ExamDetailView

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
    def setUp(self):
        author = User.objects.get_or_create(username='ss')[0]
        self.client.force_login(author)

    def test_no_exam(self):
        # If no exam exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_exam_list']), 0)

    def test_create_user_logged_in_user_with_no_exam(self):
        #    User.objects.create_user(username='ss')
        #    Login as 'ss' without password

        response = self.client.get(reverse('choice:exam-index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_exam_list']), 0)

    def test_create_user_logged_in_user_with_add_one_exam(self):
        Uauthor = User.objects.get(username='ss')
        create_exam(Uauthor, "Test exam")
        response = self.client.get(reverse('choice:exam-index'))

        self.assertEqual(len(response.context['latest_exam_list']), 1)
        self.assertContains(response, "Test exam")


class ExamDetailViews(TestCase):

    def setUp(self):
        self.author = User.objects.get_or_create(username='ss')[0]
        self.client.force_login(self.author)

    def test_exam_detail_view_not_found(self):
        url = reverse('choice:exam-detail', args=(2,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_exam_detail_view(self):
        exam = Exam.objects.create(author=self.author, title="exam_title")
        url = reverse('choice:exam-detail', args=(exam.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.context['exam_detail'], [])

        # Test if the view contains the links to the delete page, the index page and the update page
        self.assertContains(response, reverse('choice:exam-delete', args=(exam.id,)))
        self.assertContains(response, reverse('choice:exam-update', args=(exam.id,)))
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


class ExamListTemplate(TestCase):

    def test_shinki(self):
        ''' Test if ExamListView contains a set of links. '''
        response = self.client.get(reverse('choice:exam-index'))
        self.assertContains(response, reverse('choice:exam-create'))
        self.assertContains(response, reverse('admin:index'))
        self.assertContains(response, reverse('admin:logout'))


class ToRomanBadInput(unittest.TestCase):
    def test_too_large(self):
        '''to_roman should fail with large input'''

        data = {'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '2',
                'form-0-title': '',
                'form-0-url': 'http://www.yahoo.co.jp',
                'form-1-title': 'Yahoo! Japan',
                'form-1-url': 'http://www.yahoo.co.jp',
                }

        fs = BookmarkFormSet(data)
        self.assertFalse(fs.is_valid())


class ToRomanGoodInput(unittest.TestCase):
    def test_too_large(self):
        '''to_roman should pass with same input'''

        data = {'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '2',
                'form-0-title': 'Google',
                'form-0-url': 'http://www.google.com',
                'form-1-title': 'Yahoo! Japan',
                'form-1-url': 'http://www.yahoo.co.jp',
                }

        fs = BookmarkFormSet(data)
        self.assertTrue(fs.is_valid())


class QuestionFormSetGoodInput(unittest.TestCase):
    def test_good_input(self):
        '''Test if this form formset is valid '''

        data = {'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '2',
                'form-MIN_NUM_FORMS': '2',
                'form-MAX_NUM_FORMS': '100',
                'form-0-choice1': 'Google',
                'form-0-choice2': True,
                'form-1-choice1': 'Yahoo! Japan',
                'form-1-choice2': True,
                }
        fs = QuestionFormSet(data)
        self.assertTrue(fs.is_valid())

    def test_bad_input(self):
        '''Test if this formset is not valid '''

        data = {'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '2',
                'form-MIN_NUM_FORMS': '2',
                'form-MAX_NUM_FORMS': '100',
                'form-0-choice1': 'Google',
                'form-0-choice2': '',
                'form-1-choice1': 'Yahoo! Japan',
                'form-1-choice2': 'jjjj',
                }
        fs = QuestionFormSet(data)
        # self.assertFalse(fs.is_valid(), "Null and True")

        data['form-0-choice2'] = True
        data['form-1-choice2'] = ''
        fs = QuestionFormSet(data)
        # self.assertFalse(fs.is_valid(), "True and Null")

        data['form-0-choice2'] = ''
        data['form-1-choice2'] = ''
        fs = QuestionFormSet(data)
        #self.assertFalse(fs.is_valid(), "Null and Null")
