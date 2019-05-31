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
    ExamDeleteView, ExamUpdateView, \
    ExamCreateView, \
    QuestionIndexView, \
    ExamQuestionView, vote, multiple_question_form, EditQuestionView, \
    SuccessView, \
    AnswerModelFormSetView, \
    AnswerDeleteView, \
    MarkUpdateWithInlinesView, \
    MarkDeleteView


app_name = 'choice'

exam_extra_patterns = [
    path(
        '',
        ExamIndexView.as_view(),
        name='exam-list',
    ),
    path(
        '<uuid:pk>/',
        ExamDetailView.as_view(),
        name='exam-detail',
    ),
    path(
        '<uuid:pk>/update',
        ExamUpdateView.as_view(),
        name='exam-update'
    ),
    path(
        '<uuid:pk>/delete',
        ExamDeleteView.as_view(),
        name='exam-delete'
    ),
    path(
        'create/',
        ExamCreateView.as_view(),
        name='exam-create'
    ),
]

answer_extra_patterns = [
    path(
        '<uuid:pk>/',
        AnswerModelFormSetView.as_view(),
        name='answer-list',
    ),
    path(
        '<uuid:pk>/update',
        AnswerModelFormSetView.as_view(),
        name='answer-update'
    ),
    path(
        '<uuid:pk>/delete',
        AnswerDeleteView.as_view(),
        name='answer-delete'
    ),
]

mark_extra_patterns = [
    path(
        '<uuid:pk>/',
        MarkUpdateWithInlinesView.as_view(),
        name='mark-list',
    ),
    path(
        '<uuid:pk>/update',
        MarkUpdateWithInlinesView.as_view(),
        name='mark-update'
    ),
    path(
        '<uuid:pk>/delete',
        MarkDeleteView.as_view(),
        name='mark-delete'
    ),
]


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('exam/', include(exam_extra_patterns)),
    path('answer/', include(answer_extra_patterns)),
    path('mark/', include(mark_extra_patterns)),
    path('p/<uuid:pk>/', QuestionIndexView.as_view(), name='question-index'),
    path('vote/<uuid:pk>/', vote, name='exam-vote'),
    path('testform/', multiple_question_form, name='test-form'),
    path('editquestion/<uuid:pk>/', EditQuestionView.as_view(),
         name='edit-question'),
    path('success/', SuccessView.as_view(), name='success'),
]
