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

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView

from .models import Exam, Question


class ExamIndexView(generic.ListView):
    context_object_name = 'latest_exam_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Exam.objects.order_by('-created_date')[:5]


class QuestionIndexView(generic.ListView):
    model = Question
    context_object_name = 'question_list'

    def get_queryset(self):
        self.exam = get_object_or_404(Exam, id=self.kwargs['pk'])
        return Question.objects.filter(exam=self.exam)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Exam'] = self.exam
        return context


class ExamCreate(CreateView):
    model = Exam
    fields = ['title', 'author']


class ExamDetailView(DetailView):

    model = Exam
    context_object_name = 'exam_detail'


class ExamDeleteView(DeleteView):

    model = Exam
    success_url = reverse_lazy('choice:exam-index')
