"""
Copyright 2019 Akashia Shop

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

from .models import Exam


def create_exam(exam_author, exam_title):
    """
    Create a exam with tthe given exam_author and exam_title.
    """
    return Exam.objects.create(author=exam_author, title=exam_title)


class ExamIndexViews(TestCase):
    def test_no_exam(self):
        # If no exam exists, an approperiate messages is to be displayed
        response = self.client.get(reverse('choice:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No exam is available")
        self.assertQuerysetEqual(response.context['latest_exam_list'], [])

    def test_create_user_logged_in_user_with_no_exam(self):
        User.objects.create_user(username='ss')
        response = self.client.post(reverse('admin:login'), {'username': 'ss', 'password': ''})
        response = self.client.get(reverse('choice:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_exam_list'], [])

    def test_create_user_logged_in_user_with_one_exam(self):
        TEXTEXAMPLE = 'test one'
        USERNAMEEXAMPLE = 'ss'
        author = User.objects.create_user(username='ss')
        response = self.client.post(reverse('admin:login'), {'username': USERNAMEEXAMPLE, 'password': ''})
        create_exam(author, TEXTEXAMPLE)
        response = self.client.get(reverse('choice:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_exam_list'], ['<Exam: ' + TEXTEXAMPLE + '>'])
