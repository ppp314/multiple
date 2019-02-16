from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import MyExam


class IndexView(generic.ListView):
    template_name = 'exam/index.html'
    context_object_name = 'latest_exam_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return MyExam.objects.order_by('-created_date')[:5]



