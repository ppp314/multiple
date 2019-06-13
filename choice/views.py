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
from django.forms import ModelForm, inlineformset_factory
from extra_views import CreateWithInlinesView
from .models import Exam, Answer, Drill


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


class ExamCreateView(CreateWithInlinesView):
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
    template_name = 'choice/exam_update.html'
    pass


class ExamUpdateView(DetailView):
    context_object_name = 'exam_drill'
    template_name = 'choice/drill_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Must change to form.
        context['answer_list'] = Answer.objects.filter(exam=self.object)

        return context


class DrillUpdateView(DetailView):
    context_object_name = 'exam_drill'
    template_name = 'choice/drill_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Must change to form.
        context['formset'] = Drill.objects.filter(exam=self.object)

        return context


class DrillListView(DetailView):
    context_object_name = 'exam_drill'
    template_name = 'choice/drill_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['drill_list'] = Drill.objects.filter(exam=self.object)

        return context


class MarkUpdateView(DetailView):
    context_object_name = 'exam_drill'
    template_name = 'choice/drill_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Must change to form.
        context['formset'] = Drill.objects.filter(exam=self.object)

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
