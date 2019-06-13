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
from .views import HomeView, \
    AboutView, \
    SuccessView, \
    ExamListView, \
    ExamCreateView, \
    ExamUpdateView, \
    DrillUpdateView, \
    DrillListView, \
    MarkUpdateView

app_name = 'choice'

exam_extra_patterns = [
    path(
        '',
        ExamListView.as_view(),
        name='exam-list',
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

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('success/', SuccessView.as_view(), name='success'),
    path('exam/', include(exam_extra_patterns)),
    path('drill/', include(drill_extra_patterns)),
]
