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

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.forms import inlineformset_factory
from .models import Exam, Question
from .models import Bookmark
from .forms import MultipleQuestionChoiceForm
from .forms import PostCreateForm, FileFormset, MyExamForm




class ExamIndexView(generic.ListView):
    context_object_name = 'latest_exam_list'
    template_name = 'choice/exam_list.html'

    paginate_by = 10
   
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

    paginate_by = 10

    def get_queryset(self):
        self.exam = get_object_or_404(Exam, id=self.kwargs['pk'])
        return Question.objects.filter(exam=self.exam)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Exam'] = self.exam
        return context


class ExamCreate(CreateView):
    model = Exam
    fields = ['title', 'author', 'number_of_question']

    def form_valid(self, form):
        return super().form_valid(form)


class ExamDetailView(DetailView):

    model = Exam
    context_object_name = 'exam_detail'
    template_name = 'choice/detail.html'


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
            'exam_detail': exam,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_question.no += 1
        return redirect('choice:exam-index')


def testform(request):
    form = MultipleQuestionChoiceForm()

    return render(request, 'choice/name.html', {'form': form})


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。::

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def index(request):
    post_list = Bookmark.objects.order_by('-url')
    search_keyword = request.GET.get('keyword')
    if search_keyword:
        post_list = post_list.filter(title__icontains=search_keyword)

    page_obj = paginate_queryset(request, post_list, 3)

    if page_obj.number == 1:
        PostCreateFormSet = forms.modelformset_factory(
            Bookmark, form=PostCreateForm,
            extra=3, can_delete=True,)
    else:
        PostCreateFormSet = forms.modelformset_factory(
            Bookmark, form=PostCreateForm,
            extra=0, can_delete=True,)
        
    formset = PostCreateFormSet(request.POST or None,
                                queryset=page_obj.object_list)
    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return redirect('choice:test-form')

    context = {
        'formset': formset,
        'page_obj': page_obj,
    }

    return render(request, 'choice/post_formset.html', context)


def add_question(request):
    form = MyExamForm(request.POST or None)
    QuestionFormSet = inlineformset_factory(Exam, Question, fields='__all__', extra=5, max_num=5, can_delete=False)
    if request.method == 'POST' and form.is_valid():
        exam = form.save(commit=False)
        formset = QuestionFormSet(request.POST, request.FILES, instance=exam)
        if formset.is_valid():
            exam.save()
            formset.save()
            return redirect('choice:exam-index')

        else:
            formset = QuestionFormSet(request.POST, request.FILES, instance=exam)
    else:
        formset = QuestionFormSet()

    return render(request, 'choice/post_form.html',
                  {'form': form,
                   'formset': formset})


def update_post(request, pk):
    post = get_object_or_404(Bookmark, pk=pk)
    form = PostCreateForm(request.POST or None, instance=post)
    formset = FileFormset(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        # 編集ページを再度表示
        return redirect('choice:update_post', pk=pk)

    context = {
        'form': form,
        'formset': formset
    }

    return render(request, 'choice/post_form.html', context)

