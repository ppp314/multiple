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


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        pass


class TestViewHome(TestCase):
    """ Test view choice:home"""

    expected_status_code = 200
    res = None

    @property
    def response(self):
        raise NotImplementedError

    @property
    def url_to_view(self):
        raise NotImplementedError

    def setUp(self):
        self.res = self.client.get(reverse("choice:home"))

    def test_should_return_expected_return_code(self):
        self.assertEqual(self.res.status_code, self.expected_status_code)


class TestViewAbout(TestCase):
    """ Test view choice:about"""

    expected_status_code = 200

    def setUp(self):
        self.res = self.client.get(reverse("choice:about"))

    def test_should_return_expected_return_code(self):
        self.assertEqual(self.res.status_code, self.expected_status_code)


class TestViewSuccess(TestCase):
    """ Test view choice:success"""

    expected_status_code = 200

    def setUp(self):
        self.res = self.client.get(reverse("choice:success"))

    def test_should_return_expected_return_code(self):
        self.assertEqual(self.res.status_code, self.expected_status_code)


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

