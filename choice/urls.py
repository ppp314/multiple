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

from django.urls import path


from .views import (
    HomeView, AboutView, ExamIndexView, ExamDetailView, ExamDeleteView,
    ExamUpdateView, ExamCreate, QuestionIndexView, ExamQuestionView,
    vote, testform,
)

from .views import add_question

app_name = 'choice'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('mypage/', ExamIndexView.as_view(), name='exam-index'),
    path('detail/<int:pk>/',
         ExamQuestionView.as_view(), name='exam-question-view'),
    path('update/<int:pk>/', ExamUpdateView.as_view(), name='exam-update'),
    path('delete/<int:pk>/', ExamDeleteView.as_view(), name='exam-delete'),
    path('p/<int:pk>/', QuestionIndexView.as_view(), name='question-index'),
    path('new/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('vote/<int:pk>/', vote, name='exam-vote'),
    path('create/', ExamCreate.as_view(), name='exam-create'),
    path('testform/', testform, name='test-form'),
    path('addquestion/', add_question, name='add-question'),
]
