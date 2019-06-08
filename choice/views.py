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

from django.utils import timezone
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.forms import inlineformset_factory
from extra_views import CreateWithInlinesView, InlineFormSet, \
    InlineFormSetFactory, InlineFormSetView, \
    ModelFormSetView, \
    UpdateWithInlinesView
from .models import Exam, Answer, Drill
from .forms import MultipleQuestionChoiceForm
from .forms import MyExamForm
from .forms import DrillInlineFormSet


class ExamIndexView(generic.ListView):
    context_object_name = 'latest_exam_list'
    template_name = 'choice/exam_list.html'

    paginate_by = 10

    def get_queryset(self):
        """Return the last five published questions."""
        return Exam.objects.order_by('created')


class QuestionIndexView(generic.ListView):
    model = Answer
    context_object_name = 'question_list'

    paginate_by = 10

    def get_queryset(self):
        self.exam = get_object_or_404(Exam, id=self.kwargs['pk'])
        return Answer.objects.filter(exam=self.exam).order_by('no', 'sub_no')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Exam'] = self.exam
        return context


class ExamCreateView(ModelFormSetView):
    """
    Passing initial data into ModelFormSet and InlineFormSet works slightly
    differently to a regular FormSet. The data passed in from :code:`initial`
    will
    be inserted into the :code:`extra` forms of the formset. Only the data from
    :code:`get_queryset()` will be inserted into the initial rows:

    from module import symbol
    extra_views import ModelFormSetView
    from my_app.models import Item


    class ItemFormSetView(ModelFormSetView):
        template_name = 'item_formset.html'
        model = Item
        factory_kwargs = {'extra': 10}
        initial = [{'name': 'example1'}, {'name': 'example2'}]
    """
    model = Exam
    fields = [
        'author',
        'title',
    ]
    factory_kwargs = {'extra': 10}
    template_name = 'choice/exam_formset.html'


class ExamDetailView(DetailView):
    """ generic.DetailView"""
    model = Exam
    context_object_name = 'exam_detail'
    template_name = 'choice/exam_detail.html'


class ExamDeleteView(DeleteView):
    """ generic.DeleteView"""
    model = Exam
    success_url = reverse_lazy('choice:exam-list')


class ExamUpdateView(UpdateView):
    """ generic.UpdateView"""
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
        return self.object.answer_set.order_by('no', 'sub_no')


class AnswerInline(InlineFormSetFactory):
    """
    class ItemInline(InlineFormSetFactory):
        model = Item
        form_class = ItemForm
        formset_class = BaseItemFormSet
        initial = [{'name': 'example1'}, {'name', 'example2'}]
        prefix = 'item-form'
        factory_kwargs = {'extra': 2, 'max_num': None,
                          'can_order': False, 'can_delete': False}
        formset_kwargs = {'auto_id': 'my_id_%s'}
    """
    model = Answer
    fields = ('no', 'sub_no', 'point', 'correct')
    factory_kwargs = {
        'extra': 1,
        'max_num': None,
        'can_order': True,
        'can_delete': False,
    }


class AnswerModelFormSetView(UpdateWithInlinesView):
    """
    Parent: Exam
    Child: Answer
    """
    model = Exam
    inlines = [AnswerInline]
    fields = ('title', 'number_of_question')
    template_name = 'choice/answer_formset.html'

    def get_context_data(self, **kwargs):
        data = super(AnswerModelFormSetView, self).get_context_data(**kwargs)
        print("AnswerModelFormSetView:Passing get_context_data()")
        return data

    def forms_valid(self, form, inlines):
        instance = super(AnswerModelFormSetView, self).forms_valid(form, inlines)
        print("AnswerModelFormSetView:Passing forms_valid()")
        return instance


class AnswerDeleteView(generic.DeleteView):
    pass


class DrillInline(InlineFormSetFactory):
    model = Drill
    formset_class = DrillInlineFormSet
    fields = ('description',)
    factory_kwargs = {
        'extra': 1,
        'max_num': 1,
        'can_order': False,
        'can_delete': False,
    }


"""
from my_app.forms import AddressForm, BaseAddressFormSet


class AddressFormSetView(FormSetView):
    template_name = 'address_formset.html'
    form_class = AddressForm
    formset_class = BaseAddressFormSet
    initial = [{'type': 'home'}, {'type', 'work'}]
    prefix = 'address-form'
    success_url = 'success/'
    factory_kwargs = {'extra': 2, 'max_num': None,
                      'can_order': False, 'can_delete': False}
    formset_kwargs = {'auto_id': 'my_id_%s'}

from extra_views import InlineFormSetView
from my_app.models import Item
from my_app.forms import ItemForm

class ItemInlineView(InlineFormSetView):
    model = Item
    form_class = ItemForm
    formset_class = ItemInlineFormSet     # enables our custom inline
"""


class DrillCreateView(UpdateWithInlinesView):
    """
    Parent: Exam
    Child: Answer
    """
    model = Exam
    inlines = [DrillInline]
    fields = ('title', 'number_of_question')
    template_name = 'choice/drill_create.html'


class DrillUpdateWithInlinesView(UpdateWithInlinesView):
    pass


class DrillDeleteView(generic.DeleteView):
    pass


class MarkUpdateWithInlinesView(UpdateWithInlinesView):
    pass


class MarkDeleteView(generic.DeleteView):
    pass


def vote(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    try:
        selected_question = exam.answer_set.get(pk=request.POST['question'])
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'choice/detail.html', {
            'exam_detail': exam,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_question.no += 1
        return redirect('choice:exam-index')


def multiple_question_form(request):
    form = MultipleQuestionChoiceForm()

    return render(request, 'choice/name.html', {'form': form})


class EditQuestionView(InlineFormSetView):
    model = Exam
    inline_model = Answer
    template_name = 'choice/post_form.html'
    fields = ["no", "sub_no", "point", "answer"]


class HomeView(TemplateView):
    template_name = "choice/home.html"


class AboutView(TemplateView):
    template_name = "choice/about.html"


class SuccessView(TemplateView):
    template_name = "choice/success.html"


class ChildInLines(InlineFormSet):
    model = Answer
    fields = ('no', 'sub_no', 'point', )


class ParentCreateView(CreateWithInlinesView):
    model = Exam
    fields = ['title']
    context_object_name = 'exam'
    inlines = ['ChildInLines', ]
    template_name = 'choice/parent.html'
    success_url = "/"


class QuestionInlineFormSet(InlineFormSetFactory):
    model = Answer
    fields = ("no", "sub_no", "point", "answer", )
