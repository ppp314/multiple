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


from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm, inlineformset_factory, Form
from extra_views import CreateWithInlinesView, \
    UpdateWithInlinesView, \
    InlineFormSetFactory
from .models import Exam, Answer, Drill, Mark
from .models import CHOICE_MARK_CHOICES


class HomeView(TemplateView):
    template_name = "choice/home.html"


class AboutView(TemplateView):
    template_name = "choice/about.html"


class SuccessView(TemplateView):
    template_name = "choice/success.html"


class ExamListView(ListView):
    context_object_name = 'latest_exam_list'
    template_name = 'choice/exam_list.html'

    paginate_by = 10

    def get_queryset(self):
        """Return the object order by created."""
        return Exam.objects.order_by('created')


class AnswerInline(InlineFormSetFactory):
    model = Answer
    fields = ['no', 'sub_no', 'point', 'correct']


class ExamCreateView(CreateWithInlinesView):
    model = Exam
    inlines = [AnswerInline]
    fields = ['title']
    template_name = 'choice/exam_update.html'

    def get_success_url(self):
        return reverse('choice:exam-list')


class ExamUpdateView(UpdateWithInlinesView):
    model = Exam
    inlines = [AnswerInline]
    fields = ['title']
    template_name = 'choice/exam_update.html'

    def get_success_url(self):
        return reverse('choice:exam-list')


class DrillUpdateView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'choice/drill_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        DrillFormSet = inlineformset_factory(
            Exam,
            Drill,
            fields=('description',)
        )
        formset = DrillFormSet(instance=self.object)
        context['formset'] = formset

        return context


class DrillListView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'choice/drill_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Drill.objects.filter(exam=self.object)
        return context


class MarkUpdateView(DetailView):
    model = Drill
    context_object_name = 'drill'
    template_name = 'choice/mark_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        MarkFormSet = inlineformset_factory(
            Drill,
            Mark,
            fields=('your_choice',)
        )
        formset = MarkFormSet(instance=self.object)
        context['formset'] = formset

        return context


class DrillForm(ModelForm):
    class Meta:
        model = Drill
        fields = ('description',)


ExamDetailFormSet = inlineformset_factory(
    parent_model=Exam,
    model=Drill,
    form=DrillForm,
    extra=1,
    min_num=1,
    validate_min=True,
)
