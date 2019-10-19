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

from django.urls import include, path
from .views import (
    HomeView,
    AboutView,
    SuccessView,
    ExamListView,
    ExamDetailView,
    ExamCreateView,
    ExamUpdateView,
    ExamAnswerCreateView,
    DrillUpdateView,
    DrillListView,
    MarkUpdateView,
)

from .views import get_name

app_name = 'choice'

exam_extra_patterns = [
    path(
        '',
        ExamListView.as_view(),
        name='exam-list',
    ),
    path(
        '<int:pk>/',
        ExamDetailView.as_view(),
        name='exam-detail'
    ),
    path(
        '<int:pk>/update',
        ExamUpdateView.as_view(),
        name='exam-update'
    ),
    path(
        '<int:pk>/drillupdate',
        DrillUpdateView.as_view(),
        name='drill-update'
    ),
    path(
        '<int:pk>/drill',
        DrillListView.as_view(),
        name='drill-list'
    ),
    path(
        'create/',
        ExamCreateView.as_view(),
        name='exam-create'
    ),
]

drill_extra_patterns = [
    path(
        '<int:pk>/',
        MarkUpdateView.as_view(),
        name='mark-update',
    ),
]

exam_answer_extra_patterns = [
    path(
        '',
        ExamAnswerCreateView.as_view(),
        name='exam-answer-create'
    ),
    path(
        '<int:pk>/',
        ExamAnswerCreateView.as_view(),
        name='exam-answer-update'
    ),  

]
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('test/', get_name, name='test'),
    path('about/', AboutView.as_view(), name='about'),
    path('success/', SuccessView.as_view(), name='success'),
    path('exam/', include(exam_extra_patterns)),
    path('examanswer/', include(exam_answer_extra_patterns)),
    path('drill/', include(drill_extra_patterns)),
]
