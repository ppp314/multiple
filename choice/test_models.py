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
from django.contrib.auth.models import User
from .models import Exam, Question


# Create your tests here.
class TestExamModel(TestCase):
    """ Test Exam model. """
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@example.com',
            password='top_secret')
        
    def test_create_exam(self):
        self.exam = Exam.objects.create(
            author=self.user, title='Test',
            number_of_question=1)

    def test_no_exam(self):
        with self.assertRaises(Exam.DoesNotExist):
            self.exam = Exam.objects.get(author=self.user)


class TestQuestionModel(TestCase):
    """ Test Question model. """

    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@example.com',
            password='top_secret')
        self.exam = Exam.objects.create(
            author=self.user, title='Test',
            number_of_question=1)

    def test_create_question(self):
        self.question = Question.objects.create(
            exam=self.exam,
            no=1, sub_no=1, point=5,
            choice1=True,
            choice2=True,
            choice3=True,
            choice4=True,
            choice5=True)

    def test_no_question(self):
        with self.assertRaises(Question.DoesNotExist):
            self.question = Question.objects.get(exam=self.exam)
