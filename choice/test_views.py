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
from django.urls import reverse
from django.contrib.auth.models import User


class FormSetCreateViewTest(TestCase):
    """ Test if FormSet Create view contains the management form piece."""

   
class ExaamQuestionInlineViewTest(TestCase):
    """
        Test inlineformset_factory.
    """
    def test_get_exam_quesion_inline(self):
        """ Test method==GET"""
        url = reverse('choice:add-question')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'question_set-TOTAL_FORMS')
        self.assertContains(response, 'question_set-INITIAL_FORMS')
        self.assertContains(response, 'question_set-MIN_NUM_FORMS')
        self.assertContains(response, 'question_set-MAX_NUM_FORMS')

    def test_post_exam_question_inline(self):
        """ Test method==POST"""
        author = User.objects.get_or_create(username='ss')[0]

        data = {'author': author,
                'Title': "TESTURL",
                'question_set-TOTAL_FORMS': "5",
                'question_set-INITIAL_FORMS': "0",
                'question_set-MIN_NUM_FORMS': "0",
                'question_set-MAX_NUM_FORMS': "5"
                }
        url = reverse('choice:add-question')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
