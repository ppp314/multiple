"""
Copyright 2019 Acacia Shop

This file is part of Multiple.

    Multiple is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Mutliple is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Multiple.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.urls import include, path


from .views import HomeView, AboutView, ExamIndexView, ExamDetailView, \
    ExamDeleteView, ExamUpdateView, ExamCreate, QuestionIndexView, \
    ExamQuestionView, vote, multiple_question_form, EditQuestionView, \
    SuccessView

app_name = 'choice'

extra_patterns = [
    path(
        '',
        ExamIndexView.as_view(),
        name='exam-list',
    ),
    path(
        '<int:pk>/',
        ExamDetailView.as_view(),
        name='exam-detail',
    ),
    path(
        '<int:pk>/update',
        ExamUpdateView.as_view(),
        name='exam-update'
    ),
    path(
        '<int:pk>/delete',
        ExamDeleteView.as_view(),
        name='exam-delete'
    ),
]


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('exam/', include(extra_patterns)),
    path('p/<int:pk>/', QuestionIndexView.as_view(), name='question-index'),
    path('vote/<int:pk>/', vote, name='exam-vote'),
    path('create/', ExamCreate.as_view(), name='exam-create'),
    path('testform/', multiple_question_form, name='test-form'),
    path('editquestion/<int:pk>', EditQuestionView.as_view(),
         name='edit-question'),
    path('success/', SuccessView.as_view(), name='success'),
]
