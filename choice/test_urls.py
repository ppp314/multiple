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
from django.urls.base import resolve, Resolver404
from .views import HomeView, AboutView, ExamIndexView, \
    ExamCreateView, \
    ExamUpdateView, ExamDeleteView, QuestionIndexView,  ExamDetailView, \
    AnswerModelFormSetView, \
    AnswerDeleteView, \
    MarkUpdateWithInlinesView, \
    MarkDeleteView, \
    vote, \
    multiple_question_form, \
    EditQuestionView, \
    SuccessView


@pytest.mark.parametrize("test_url, expected", [
    ('/', HomeView),
    ('/about/', AboutView),
    ('/exam/', ExamIndexView),
    ('/exam/create/', ExamCreateView),
    ('/exam/3539427c-9f18-44a7-844f-7ca13c7d922f/', ExamDetailView),
    ('/exam/3539427c-9f18-44a7-844f-7ca13c7d922f/update', ExamUpdateView),
    ('/exam/3539427c-9f18-44a7-844f-7ca13c7d922f/delete', ExamDeleteView),
    ('/answer/3539427c-9f18-44a7-844f-7ca13c7d922f/', AnswerModelFormSetView),
    ('/answer/3539427c-9f18-44a7-844f-7ca13c7d922f/update', AnswerModelFormSetView),
    ('/answer/3539427c-9f18-44a7-844f-7ca13c7d922f/delete', AnswerDeleteView),
    ('/mark/3539427c-9f18-44a7-844f-7ca13c7d922f/', MarkUpdateWithInlinesView),
    ('/mark/3539427c-9f18-44a7-844f-7ca13c7d922f/update', MarkUpdateWithInlinesView),
    ('/mark/3539427c-9f18-44a7-844f-7ca13c7d922f/delete', MarkDeleteView),
    ('/p/3539427c-9f18-44a7-844f-7ca13c7d922f/', QuestionIndexView),
    ('/vote/3539427c-9f18-44a7-844f-7ca13c7d922f/', vote),
    ('/testform/', multiple_question_form),
    ('/editquestion/3539427c-9f18-44a7-844f-7ca13c7d922f/', EditQuestionView),
    ('/success/', SuccessView),
])
def test_urls_valid(test_url, expected):
    """
    Test if the given test_url can be resolved.
    The preceding slashes and trailing slashes are significant.
    """
    match = resolve(test_url)
    assert match.func.__name__ == expected.__name__


def test_urls_invalid():
    """
    Test if the given fake test_url can not be resolved.
    The preceding slashes and trailing slashes are significant.
    """
    with pytest.raises(Resolver404):
        resolve('/error404/')
