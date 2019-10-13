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


from django.views.generic import TemplateView, ListView, View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.forms import ModelForm, inlineformset_factory, Form
from extra_views import CreateWithInlinesView, \
    UpdateWithInlinesView, \
    InlineFormSetFactory
from .models import Exam, Answer, Drill, Mark
from .models import CHOICE_MARK_CHOICES
from .forms import ExampleFormSetHelper
from .forms import ArticleForm


class HomeView(TemplateView):
    template_name = "choice/home.html"


class AboutView(TemplateView):
    template_name = "choice/about.html"


class SuccessView(TemplateView):
    template_name = "choice/success.html"


class ExamListView(ListView):
    """ Exam Generic ListView"""
    model = Exam
    paginate_by = 10


class AnswerInline(InlineFormSetFactory):
    model = Answer
    fields = ['no', 'sub_no', 'point', 'correct']


class ExamCreateView(CreateWithInlinesView):
    model = Exam
    inlines = [AnswerInline]
    fields = ['title']
    template_name = 'choice/exam_update.html'

    def get_success_url(self):
        """ Return the url when ExamCreateView succeeds."""
        return reverse('choice:exam-list')


class ExamUpdateView(UpdateWithInlinesView):
    model = Exam
    inlines = [AnswerInline]
    fields = ['title']
    template_name = 'choice/exam_update.html'

    def get_success_url(self):
        """ Return the url when ExamUpdateView succeeds."""
        return reverse('choice:exam-list')


class DrillUpdateGetView(DetailView):
    """ The Generic class used to render initial form.

    Parent class is Exam.
    """
    model = Exam
    context_object_name = 'exam'
    template_name = 'choice/drill_update.html'

    def get_context_data(self, **kwargs):
        """ Return context for the DetailView as well as DrillFormset and FormHelper.

        Returns:
            context: dictionary of formset and helper
            ::
                {
                    'formset': DrillFormSet,
                    'helper: crispy_forms helper,
                }

        """
        context = super().get_context_data(**kwargs)

        DrillFormSet = inlineformset_factory(
            Exam,
            Drill,
            fields=('description',)
        )
        formset = DrillFormSet(instance=self.object)
        context['formset'] = formset
        helper = ExampleFormSetHelper()
        context['helper'] = helper

        return context


class DrillUpdatePostView(SingleObjectMixin, View):
    """ The generic SingleObjct class providing the post function."""
    model = Exam

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        DrillFormSet = inlineformset_factory(
            Exam,
            Drill,
            fields=('description',)
        )
        formset = DrillFormSet(request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                reverse(
                    'choice:drill-list',
                    kwargs={'pk': self.object.pk}
                )
            )


class DrillUpdateView(View):
    """ Dispatch get and post fuction as requested."""
    def get(self, request, *args, **kwargs):
        view = DrillUpdateGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DrillUpdatePostView.as_view()
        return view(request, *args, **kwargs)


class DrillListView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'choice/drill_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Drill.objects.filter(exam=self.object)
        return context


class MarkUpdateGetView(DetailView):
    """ The Generic class used to render initial form.

    Parent class is Drill
    """
    model = Drill
    context_object_name = 'drill'
    template_name = 'choice/mark_update.html'

    def get_context_data(self, **kwargs):
        """ Return context_data as usual as well as MarkFormset.

        Returns:
            context: the dictionary of formset.
            ::
                {
                    'formset': MarkFormSet,
                }

        """
        context = super().get_context_data(**kwargs)
        MarkFormSet = inlineformset_factory(
            Drill,
            Mark,
            fields=('your_choice', 'answer')
        )
        formset = MarkFormSet(instance=self.object)
        context['formset'] = formset

        return context


class MarkUpdatePostView(SingleObjectMixin, View):
    """ The generic SingleObjct class providing post fuction."""
    model = Drill

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        MarkFormSet = inlineformset_factory(
            Drill,
            Mark,
            fields=('your_choice', 'answer')
        )
        formset = MarkFormSet(request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                reverse(
                    'choice:drill-list',
                    kwargs={'pk': self.object.pk}
                )
            )


class MarkUpdateView(View):
    """ Dispatch get and post fuction as requested."""
    def get(self, request, *args, **kwargs):
        view = MarkUpdateGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MarkUpdatePostView.as_view()
        return view(request, *args, **kwargs)


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


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArticleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            newarticle = form.save(commit=False)
            newarticle.headline = 'post'
            newarticle.save()

            form.save()
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('success/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArticleForm()

    return render(request, 'choice/name.html', {'form': form})

def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000

    It must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ...
    OverflowError: n too large
    """

    import math
    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result
