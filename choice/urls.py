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

from django.urls import path


from .views import ExamIndexView, ExamDetailView, ExamDeleteView, ExamUpdateView, ExamCreate, QuestionIndexView, ExamQuestionView, ExamTrialView, vote, testform

app_name = 'choice'

urlpatterns = [
   path('', ExamIndexView.as_view(), name='exam-index'),
   path('<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
   path('update/<int:pk>/', ExamUpdateView.as_view(), name='exam-update'),
   path('delete/<int:pk>/', ExamDeleteView.as_view(), name='exam-delete'),
   path('p/<int:pk>/', QuestionIndexView.as_view(), name='question-index'),
   path('new/<int:pk>/', ExamQuestionView.as_view(), name='exam-question-view'),
   path('vote/<int:pk>/', vote, name='exam-vote'),
   path('create/', ExamCreate.as_view(), name='exam-create'),
   path('testform/', testform, name='test-form'),
]
