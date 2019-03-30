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
from .models import Exam, Question

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    ordering = ['no', 'sub_no']


class MyExamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author']}),
        ('Contents of Exam created_date',
         {'fields': ['created_date']}),
        ('Contents of Exam title',
         {'fields': ['title']}),

        ]
    inlines = [QuestionInline]
    list_display = ('pk', 'author', 'created_date', 'title')


admin.site.register(Exam, MyExamAdmin)
admin.site.register(Question)
