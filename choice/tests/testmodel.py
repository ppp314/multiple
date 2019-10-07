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
import doctest
from django.test import TestCase
from django.urls import reverse
from .. import models, views


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        pass


class HomeViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('choice:home'))
        self.assertEqual(response.status_code, 200)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(models))
    tests.addTests(doctest.DocTestSuite(views))

    return tests
