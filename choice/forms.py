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

from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from django.utils import timezone
from .models import Exam, Answer, Drill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class MultipleQuestionChoiceForm(forms.Form):
    foo_select = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foo_select'].queryset = Exam.objects.all()


class ExamForm(forms.Form):
    class Meta:
        model = Exam
        fields = ['title', 'number_of_question']


class QuestionForm(forms.Form):
    class Meta:
        model = Answer
        fields = ['no', 'sub_no', 'point']


class MyExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    q_tobemade = forms.IntegerField(
        max_value=60,
        min_value=1,
    )


class DrillInlineFormSet(BaseInlineFormSet):
    def clean(self):
        print("DrillInlineFormSet: passing clean() method.")
        super().clean()
        # example custom validation across forms in the formset
        asof = timezone.now()
        for form in self.forms:
            form.cleaned_data['created'] = asof
            # update the instance value, too.
            form.instance.name = asof


class ExampleFormSetHelper(FormHelper):
    """Return FormHelper from crispy_forms."""
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_class = 'form-inline'
        self.render_required_fields = True
        self.add_input(Submit("submit", "Save"))
