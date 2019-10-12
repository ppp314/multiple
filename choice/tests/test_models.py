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
from ..models import Exam
from .factories import ExamFactory


class TestExamModel(TestCase):
    """ Test Exam model"""

    def setUp(self):
        factory = ExamFactory
        factory.create_batch(size=2)

    def test_should_have_number_of_exam(self):
        self.assertEqual(Exam.objects.count(), 2)

    def test_should_not_create_model(self):
        with self.assertRaises(TypeError):
            Exam.objects.create(tite="")
