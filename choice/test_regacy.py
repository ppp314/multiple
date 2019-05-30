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

import pytest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Exam, Answer
import unittest


# Create your tests here.



TEXTEXAMPLE = 'test one'


def create_exam(exam_author, exam_title):
    """
    Create a exam with tthe given exam_author and exam_title.
    """
    return Exam.objects.create(author=exam_author, title=exam_title)


class TestExamIndexViewsNoExam(TestCase):
    def test_no_exam(self):
        ''' If no exam exists, an approperiate messages is to be displayed '''
        response = self.client.get(reverse('choice:exam-list'))
        self.assertContains(response, "No exam is available")
        self.assertQuerysetEqual(response.context['latest_exam_list'], [])


class TestExamDetailViews(TestCase):

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
        self.assertContains(response, reverse('choice:exam-list'))
        self.assertTemplateUsed(response, 'choice/detail.html')


class TestExamListTemplate(TestCase):

    def test_shinki(self):
        ''' Test if ExamListView contains a set of links. '''
        response = self.client.get(reverse('choice:exam-list'))
        self.assertContains(response, reverse('admin:index'))
        self.assertContains(response, reverse('admin:logout'))

