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

from .views import \
    DrillCreateView, \
    DrillUpdateWithInlinesView, \
    DrillDeleteView


app_name = 'choice'

exam_extra_patterns = [
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
    path(
        'create/',
        ExamCreateView.as_view(),
        name='exam-create'
    ),
]

answer_extra_patterns = [
    path(
        '<int:pk>/',
        AnswerModelFormSetView.as_view(),
        name='answer-list',
    ),
    path(
        '<int:pk>/update',
        AnswerModelFormSetView.as_view(),
        name='answer-update'
    ),
    path(
        '<int:pk>/delete',
        AnswerDeleteView.as_view(),
        name='answer-delete'
    ),
]

drill_extra_patterns = [
    path(
        '<int:pk>/create',
        DrillCreateView.as_view(),
        name='drill-create',
    ),
    path(
        '<int:pk>/',
        DrillUpdateWithInlinesView.as_view(),
        name='drill-list',
    ),
    path(
        '<int:pk>/update',
        DrillUpdateWithInlinesView.as_view(),
        name='drill-update'
    ),
    path(
        '<int:pk>/delete',
        DrillDeleteView.as_view(),
        name='drill-delete'
    ),
]

mark_extra_patterns = [
    path(
        '<int:pk>/',
        DrillUpdateWithInlinesView.as_view(),
        name='drill-list',
    ),
    path(
        '<int:pk>/update',
        DrillUpdateWithInlinesView.as_view(),
        name='drill-update'
    ),
    path(
        '<int:pk>/delete',
        DrillDeleteView.as_view(),
        name='drill-delete'
    ),
]

mark_extra_patterns = [
    path(
        '<int:pk>/',
        MarkUpdateWithInlinesView.as_view(),
        name='mark-list',
    ),
    path(
        '<int:pk>/update',
        MarkUpdateWithInlinesView.as_view(),
        name='mark-update'
    ),
    path(
        '<int:pk>/delete',
        MarkDeleteView.as_view(),
        name='mark-delete'
    ),
]


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('exam/', include(exam_extra_patterns)),
    path('answer/', include(answer_extra_patterns)),
    path('drill/', include(drill_extra_patterns)),
    path('mark/', include(mark_extra_patterns)),
    path('p/<int:pk>/', QuestionIndexView.as_view(), name='question-index'),
    path('vote/<int:pk>/', vote, name='exam-vote'),
    path('testform/', multiple_question_form, name='test-form'),
    path('editquestion/<int:pk>', EditQuestionView.as_view(),
         name='edit-question'),
    path('success/', SuccessView.as_view(), name='success'),
]
