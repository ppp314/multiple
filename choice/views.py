"""
Copyright 2019 Akashia Shop

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

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Exam


class IndexView(generic.ListView):
    template_name = 'exam/index.html'
    context_object_name = 'latest_exam_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Exam.objects.order_by('-created_date')[:5]

