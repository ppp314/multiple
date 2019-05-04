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


from django.urls.base import resolve
from .views import HomeView, AboutView, ExamIndexView, ExamQuestionView


@pytest.mark.parametrize("test_url, expected", [
    ("/", HomeView),
    ("/about/", AboutView),
    ("/list/", ExamIndexView),
    ("/detail/1/", ExamQuestionView),
])
def test_urls_valid(test_url, expected):
    match = resolve(test_url)
    assert match.func.__name__ == expected.__name__
