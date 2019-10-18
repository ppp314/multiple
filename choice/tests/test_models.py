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
from ..models import Exam, Answer
from .factories import ExamFactory, AnswerFactory


class TestExamModel(TestCase):
    """ Test Exam model"""

    def test_should_have_number_of_exam(self):
        exam = ExamFactory()
        AnswerFactory.create_batch(size=20, exam=exam)
        self.assertEqual(Answer.objects.count(), 20)

    def test_should_return_absolute_url(self):
        e = ExamFactory()
        url = e.get_absolute_url()
        self.assertEqual(url, '/exam/' + str(e.pk) + '/')

    def test_should_not_create_model(self):
        with self.assertRaises(TypeError):
            Exam.objects.create(tite="")

    def test_should_have_answer_count(self):
        exam = ExamFactory()
        AnswerFactory.create_batch(size=20, exam=exam)

        self.assertEqual(20, Exam.objects.first().answer__count)
