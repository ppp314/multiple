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

import factory
from ..models import Exam, Answer
from ..models import Drill, Mark
from ..models import CHOICE_MARK_ONE, CHOICE_MARK_TWO


class ExamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exam

    title = factory.Sequence(lambda n: "Exam %03d" % n)
    number_of_question = 10


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    no = factory.Sequence(lambda n: n)
    sub_no = 1

    point = 5
    correct = CHOICE_MARK_ONE

    exam = factory.SubFactory(ExamFactory)


class DrillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Drill

    exam = factory.SubFactory(ExamFactory)
    description = str(factory.Sequence(lambda n: n))


class MarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mark

    drill = factory.SubFactory(DrillFactory)
    answer = factory.SubFactory(AnswerFactory)
    your_choice = CHOICE_MARK_TWO
