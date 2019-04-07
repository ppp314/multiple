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
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, formset_factory
from .models import Exam, Question
from .models import Bookmark, BookmarkForm, BaseBookmarkFormSet
from .forms import QuestionForm


# Create your tests here.
class ExamModel(TestCase):
    """
    Test a view function the same way as you would test any other
    fuction
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@example.com',
            password='top_secret')
        self.exam = Exam.objects.create(
            author=self.user, title='Test',
            number_of_question=1)
        self.question = Question.objects.create(
            exam=self.exam, no=1,
            sub_no=1, point=5)

    def test_exam(self):
        jacob = Exam.objects.get(author=self.user)
        self.assertEquals(jacob.title, 'Test')

    def test_question(self):
        q = Question.objects.get(exam=self.exam)
        self.assertEquals(q.point, 5)

    def test_exam_question_formset(self):
        QuestionFormSet = inlineformset_factory(
            parent_model=Exam,
            model=Question,
            form=QuestionForm,
            extra=1,
            min_num=1)
        exam = Exam.objects.get(author=self.user)

        #formset = QuestionFormSet()

        #self.assertTrue(formset.is_valid())

    def test_book_mark_Formset(self):
        self.bookmark = Bookmark.objects.create(
            title='Django project',
            url='http://www.google.com/')

        BookmarkFormSet = formset_factory(
            BookmarkForm, formset=BaseBookmarkFormSet,
            extra=1, max_num=1)
        fs=BookmarkFormSet(
                {'form-TOTAL_FORMS': '1',
                 'form-INITIAL_FORMS': '1',
                 'form-MIN_NUM_FORMS': '1',
                 'form-MAX_NUM_FORMS': '1',
                 'form-0-title': 'Django is now open ',
                 'form-0-url': 'http://www'})
        self.assertTrue(fs.is_valid())
