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
from .models import Exam, CorrectAns, Drill, Answer

# Register your models here.


class CorrectAnsInline(admin.TabularInline):
    model = CorrectAns
    extra = 0
    ordering = ['no', 'sub_no']


class DrillInline(admin.TabularInline):
    model = Drill
    extra = 0
    ordering = ['title']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    ordering = ['correctans__no', 'correctans__sub_no']


class MyExamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author']}),
        ('Contents of Exam created_date',
         {'fields': ['created_date']}),
        ('Contents of Exam title',
         {'fields': ['title']}),

        ]

    list_display = ('pk', 'author', 'created_date', 'title')
    inlines = [CorrectAnsInline, DrillInline]


admin.site.register(Exam, MyExamAdmin)
