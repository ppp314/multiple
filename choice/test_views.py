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
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Exam, Drill
from .forms import MyExamForm
from .views import ExamCreateView, get_name
from .models import Publication, Article

@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_url,expected_template", [
        ("choice:home",
         ["choice/home.html", "choice/base.html"]),
        ("choice:about",
         ["choice/about.html", "choice/base.html"]),
        ("choice:success",
         ["choice/success.html", "choice/base.html"]),
        ('choice:exam-list',
         ["choice/exam_list.html", "choice/base.html"]),
        ('choice:exam-create',
         ["choice/exam_update.html", "choice/base.html"]),
    ],)
def test_get_simple_view(client, test_url, expected_template):
    """ Test if the page about is pavailable"""
    url = reverse(test_url)
    response = client.get(url)
    for e in expected_template:
        assert e in [t.name for t in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_url,expected_template", [
        ('choice:exam-update',
         ["choice/exam_update.html", "choice/base.html"]),
        ('choice:drill-update',
         ["choice/drill_update.html", "choice/base.html"]),
        ('choice:drill-list',
         ["choice/drill_list.html", "choice/base.html"]),
    ],)
def test_get_exam_onearg_view(
        create_user_exam_fixture, client, test_url, expected_template):
    """Test if the view which requires id argument is available."""
    id = Exam.objects.first().id
    url = reverse(test_url, args=(id,))
    response = client.get(url)
    assert response.status_code == 200
    for e in expected_template:
        assert e in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_url,expected_template", [
        ('choice:mark-update',
         ["choice/mark_update.html", "choice/base.html"]),
    ],)
def test_get_drill_onearg_view(
        create_user_exam_fixture, client, test_url, expected_template):
    """Test if the view which requires id argument is available."""
    id = Drill.objects.first().id
    url = reverse(test_url, args=(id,))
    response = client.get(url)
    assert response.status_code == 200
    for e in expected_template:
        assert e in [t.name for t in response.templates]


@pytest.mark.skip
@pytest.mark.django_db
def test_create_exam_form_valid():
    assert Exam.objects.count() == 0
    test_author = User.objects.create_user(
        username='jacob',
        email='jacob@example.com',
        password='top_secret'
    )

    form_data = {
        'title': "Test One",
        'author': test_author.id,
        'created': timezone.now(),
        'number_of_question': 10,
        'q_tobemade': 15,
    }

    form = MyExamForm(data=form_data)
    print(form.errors)
    assert form.is_valid()


@pytest.mark.skip
@pytest.mark.django_db
def test_create_exam_by_post(rf):
    assert Exam.objects.count() == 0
    test_author = User.objects.create_user(
        username='jacob',
        email='jacob@example.com',
        password='top_secret'
    )

    """
    def test_details(rf):
        request = rf.get('/customer/details')
        response = my_view(request)
        assert response.status_code == 200

    """
    url = reverse('choice:exam-create')
    request = rf.get(url)
    response = ExamCreateView.as_view()(request)
    assert response.status_code == 200

    """
    The value of response.rendered_content is following.
    <input type="hidden" name="form-TOTAL_FORMS" value="10"
        id="id_form-TOTAL_FORMS">
    <input type="hidden" name="form-INITIAL_FORMS" value="0"
        id="id_form-INITIAL_FORMS">
    <input type="hidden" name="form-MIN_NUM_FORMS" value="0"
        id="id_form-MIN_NUM_FORMS">
    <input type="hidden" name="form-MAX_NUM_FORMS" value="1000"
        id="id_form-MAX_NUM_FORMS">
    """

    before = Exam.objects.count()

    test_data = {
        'form-TOTAL_FORMS': "10",
        'form-INITIAL_FORMS': "0",
        'form-MIN_NUM_FORMS': "0",
        'form-MAX_NUM_FORMS': "1000",
        'form-0-author': test_author.id,
        'form-0-title': "Success test",
    }
    url = reverse('choice:exam-create')
    request = rf.post(url, data=test_data)
    response = ExamCreateView.as_view()(request)
    assert response.status_code == 302

    after = Exam.objects.count()

    assert before + 1 == after


@pytest.mark.django_db
def test_article_get(rf, create_publication):
    url = reverse('choice:test')
    request = rf.get(url)
    response = get_name(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_article_post(rf, create_publication):
    publication = Publication.objects.first()
    test_data = {
        'headline': "Succeed",
        'publications': publication.id
    }
    url = reverse('choice:test')
    request = rf.post(url, data=test_data)
    response = get_name(request)
    assert response.status_code == 302
