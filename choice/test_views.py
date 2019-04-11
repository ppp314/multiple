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


class FormSetCreateViewTest(TestCase):
    """ Test if FormSet Create view contains the management form piece."""
    def test_exam_detail_view_not_found(self):
        url = reverse('choice:test-formset')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'INITIAL_FORMS')
        self.assertContains(response, 'TOTAL_FORMS')


class InlineViewTest(TestCase):
    """
        Test inlineformset_factory.
    """
    def test_file_formset(self):
        url = reverse('choice:add-post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'INITIAL_FORMS')
        self.assertContains(response, 'TOTAL_FORMS')

    def test_add_post(self):
        """ test if calling post on inline formset results in redirect"""
        data = {'title': "TESTTITLE",
                'url': "TESTURL",
                'file_set-TOTAL_FORMS': "5",
                'file_set-INITIAL_FORMS': "0",
                'file_set-MIN_NUM_FORMS': "0",
                'file_set-MAX_NUM_FORMS': "5"
                }
        url = reverse('choice:add-post')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
