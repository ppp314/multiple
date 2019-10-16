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

from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Exam, Answer, Drill, Publication, Article
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


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ()


AnswerFormSet = inlineformset_factory(Exam, Answer,
                                      form=AnswerForm, extra=1)


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


class ArticleForm(ModelForm):
    """ArticleForm class for ManyToManyField sample.

    From Django documentation.
    """

    class Meta:
        model = Article
        fields = ('headline', 'publications')
