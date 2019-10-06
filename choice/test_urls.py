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

import pytest
from django.urls.base import resolve, Resolver404
from .views import HomeView, AboutView, SuccessView, \
    ExamListView, \
    ExamCreateView, \
    ExamUpdateView, \
    DrillUpdateView, \
    DrillListView, \
    MarkUpdateView


@pytest.mark.parametrize("test_url, expected", [
    ('/', HomeView),
    ('/about/', AboutView),
    ('/success/', SuccessView),
    ('/exam/', ExamListView),
    ('/exam/create/', ExamCreateView),
    ('/exam/1/update', ExamUpdateView),
    ('/exam/1/drillupdate', DrillUpdateView),
    ('/exam/1/drill', DrillListView),
    ('/drill/1/', MarkUpdateView),
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
