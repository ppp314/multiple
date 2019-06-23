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
