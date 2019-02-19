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

from django.contrib import admin
from .models import Exam, Question, Choice

# Register your models here.


class ChoiceInline(admin.StackedInline):
    model = Choice


class QuestionInline(admin.StackedInline):
    model = Question



class MyExamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author']}),
        ('Contents of Exam created_date',
             {'fields': ['created_date']}),
        ('Contents of Exam title',
             {'fields': ['title']}),

        ]
    inlines = [QuestionInline]


admin.site.register(Exam, MyExamAdmin)
