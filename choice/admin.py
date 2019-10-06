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
from .models import Exam, Answer, Drill, Mark

# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    ordering = ['no', 'sub_no']


class DrillInline(admin.TabularInline):
    model = Drill
    extra = 0
    ordering = ['id']

  
class MarkInline(admin.TabularInline):
    model = Mark
    extra = 0
    ordering = ['answer__no', 'answer__sub_no']


class MyExamAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Contents of Exam created',
         {'fields': ['created']}),
        ('Contents of Exam title',
         {'fields': ['title']}),

        ]

    list_display = ('pk', 'created', 'title')
    inlines = [AnswerInline, DrillInline]


admin.site.register(Exam, MyExamAdmin)
