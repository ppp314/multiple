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
import unittest

from django.test import TestCase

from .factories import ExamFactory, AnswerFactory, DrillFactory, MarkFactory
from ..models import CHOICE_MARK_ONE, CHOICE_MARK_TWO


class TestExamModel(TestCase):
    """ Test Exam model"""

    def test_should_have_number_of_exam(self):
        from ..models import Answer

        exam = ExamFactory()
        AnswerFactory.create_batch(size=20, exam=exam)
        self.assertEqual(Answer.objects.count(), 20)

    def test_should_return_absolute_url(self):
        e = ExamFactory()
        url = e.get_absolute_url()
        self.assertEqual(url, '/exam/' + str(e.pk) + '/')

    def test_should_not_create_model(self):
        from ..models import Exam
        with self.assertRaisesMessage(
                TypeError,
                "Exam() got an unexpected keyword argument 'tite'",
        ):
            Exam.objects.create(tite="")

    def test_maneger_should_have_answer_count(self):
        from ..models import Exam

        size = 20
        exam = ExamFactory()
        AnswerFactory.create_batch(size=size, exam=exam)

        self.assertEqual(size, Exam.objects.first().answer__count)

    def test_manager_should_have_answer_point_sum(self):
        from ..models import Exam

        size = 20
        point = 10
        exam = ExamFactory()
        AnswerFactory.create_batch(size=size, point=point, exam=exam)

        self.assertEqual(size * point, Exam.objects.first().answer__point__sum)


class TestDrillModel(TestCase):
    """Test Drill Model."""

    def test_should(self):
        from ..models import Drill
        exam = ExamFactory()
        answer = AnswerFactory(exam=exam)
        drill = DrillFactory(exam=exam)
        mark = MarkFactory(
            drill=drill,
            answer=answer,
            your_choice=CHOICE_MARK_TWO
        )

        d = Drill.objects.get(pk=drill.id)


class TestMarkModel(TestCase):
    """Test Mark Model."""

    def test_should_create_model(self):
        from ..models import Mark

        exam = ExamFactory()
        answer = AnswerFactory(exam=exam)
        drill = DrillFactory(exam=exam)
        your_choice = CHOICE_MARK_ONE

        mark = Mark.objects.create_mark(
            drill=drill,
            answer=answer,
            your_choice=your_choice,
        )

        self.assertEqual(mark.drill, drill)
        self.assertEqual(mark.answer, answer)
        self.assertEqual(mark.your_choice, your_choice)

