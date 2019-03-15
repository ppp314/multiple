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
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin

from .models import Exam, Question
from .forms import MultipleQuestionChoiceForm


class ExamIndexView(generic.ListView):
    context_object_name = 'latest_exam_list'
    template_name = 'choice/exam_list.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Exam.objects.order_by('-created_date')


class ExamTrialView(generic.ListView):
    template_name = 'choice/exam_list.html'

    def get_queryset(self):
        return Exam.objects.question_set.all()


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


class ExamUpdateView(UpdateView):

    model = Exam
    fields = ['title', 'author']


class ExamQuestionView(SingleObjectMixin, generic.ListView):
    template_name = "choice/exam_question_list.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Exam.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = self.object
        return context

    def get_queryset(self):
        return self.object.question_set.all()


def vote(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    try:
        selected_question = exam.question_set.get(pk=request.POST['question'])
    except (KeyError, Question.DoesNotExist):
        return render(request, 'choice/detail.html', {
            'exam': exam,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_question.no += 1
        return redirect('choice:exam-index')


def testform(request):
    form = MultipleQuestionChoiceForm()

    return render(request, 'choice/name.html', {'form': form})
