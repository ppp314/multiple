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
from django.urls import reverse
from ..models import Answer, Exam
from .factories import ExamFactory, AnswerFactory


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        pass


class TestViewHome(TestCase):
    """ Test view choice:home"""
    def _getTarget(self):
        return reverse('choice:home')

    def test_should_return_expected_return_code(self):
        self.res = self.client.get(self._getTarget())
        self.assertEqual(self.res.status_code, 200)


class TestViewAbout(TestCase):
    """ Test view choice:about"""
    def _getTarget(self):
        return reverse('choice:about')

    def test_should_return_expected_return_code(self):
        self.res = self.client.get(self._getTarget())
        self.assertEqual(self.res.status_code, 200)


class TestViewSuccess(TestCase):
    """ Test view choice:success"""
    def _getTarget(self):
        return reverse('choice:success')

    def test_should_return_expected_return_code(self):
        self.res = self.client.get(self._getTarget())
        self.assertEqual(self.res.status_code, 200)


class TestViewExamlist(TestCase):
    """ Test view choice:exam-list"""

    expected_status_code = 200

    def setUp(self):
        self.res = self.client.get(reverse("choice:exam-list"))

    def test_should_return_expected_return_code(self):
        self.assertEqual(self.res.status_code, self.expected_status_code)


class TestViewExamcreate(TestCase):
    """ Test view choice:exam-create"""

    expected_status_code = 200

    def setUp(self):
        self.res = self.client.get(reverse("choice:exam-create"))

    def test_should_return_expected_return_code(self):
        self.assertEqual(self.res.status_code, self.expected_status_code)


class TestExamListView(TestCase):

    def _getTarget(self):
        return reverse('choice:exam-list')

    def test_exam_not_available(self):
        res = self.client.get(self._getTarget())

        self.assertContains(res, "No exam is available.")
        self.assertEqual(res.status_code, 200)

    def test_exam_item(self):
        ExamFactory()
        res = self.client.get(self._getTarget())

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_list.html')
        self.assertTemplateUsed(res, 'choice/base.html')


class TestExamDetailView(TestCase):

    def _getTarget(self, pk):
        return reverse('choice:exam-detail', kwargs={'pk': pk})

    def test_exam_not_available(self):
        res = self.client.get(self._getTarget(1))
        self.assertEqual(res.status_code, 404)

    def test_exam_item(self):
        exam = ExamFactory()
        res = self.client.get(self._getTarget(exam.id))

        self.assertEqual(exam.id, res.context['exam'].id)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_detail.html')
        self.assertTemplateUsed(res, 'choice/base.html')


class TestExamCreateView(TestCase):

    def _getTarget(self):
        return reverse('choice:exam-create')

    def test_exam_create_get(self):
        res = self.client.get(self._getTarget())

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_form.html')
        self.assertTemplateUsed(res, 'choice/base.html')

    def test_exam_create_post(self):
        res = self.client.post(self._getTarget(), {'no': 1, 'number_of_question': 10})

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_form.html')
        self.assertTemplateUsed(res, 'choice/base.html')


class TestExamUpdateView(TestCase):

    def _getTarget(self, pk):
        return reverse('choice:exam-update', kwargs={'pk': pk})

    def test_exam_update_get(self):
        exam = ExamFactory()
        res = self.client.get(self._getTarget(exam.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_form.html')
        self.assertTemplateUsed(res, 'choice/base.html')

    def test_exam_update_post(self):
        exam = ExamFactory()
        res = self.client.post(self._getTarget(exam.id), {'no': 1, 'number_of_question': 10})

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_form.html')
        self.assertTemplateUsed(res, 'choice/base.html')


class TestExamAnswerCreateView(TestCase):

    def _getTarget(self):
        return reverse('choice:exam-answer-create')

    def test_exam_create_get(self):
        res = self.client.get(self._getTarget())

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_answer_formset.html')
        self.assertTemplateUsed(res, 'choice/base.html')


class TestExamAnswerUpdateView(TestCase):

    def _getTarget(self, pk):
        return reverse('choice:exam-answer-update', kwargs={'pk': pk})

    def test_exam_update_get(self):
        exam = ExamFactory()
        AnswerFactory.create_batch(size=20, exam=exam)
        res = self.client.get(self._getTarget(exam.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_answer_formset.html')
        self.assertTemplateUsed(res, 'choice/base.html')

    @unittest.skip("Unable test post data. Skipping")
    def test_exam_update_post(self):
        exam = ExamFactory()
        AnswerFactory.create_batch(size=20, exam=exam)
        data = {
            "answer_set-TOTAL_FORMS": "21",
            "answer_set-INITIAL_FORMS": "20",
            "answer_set-MIN_NUM_FORMS": "0",
            "answer_set-MAX_NUM_FORMS": "1000",
            "title": "First Test",
        }
        res = self.client.post(self._getTarget(exam.id), data)

        e = Exam.objects.get(id=exam.id)
        self.assertEqual("First Test", e.title)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'choice/exam_answer_formset.html')
        self.assertTemplateUsed(res, 'choice/base.html')
