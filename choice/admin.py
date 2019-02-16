# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import MyExam, MyChoice

# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = MyChoice
    
class MyExamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, { 'fields': ['author']}),
        ('Contents of MyExam created_date',
             { 'fields': ['created_date']}),
        ('Contents of MyExm title',
             { 'fields': ['title']}),

        ]
    inlines = [ChoiceInline]
        
admin.site.register(MyExam, MyExamAdmin)
