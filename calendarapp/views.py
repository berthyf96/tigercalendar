# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse

from .models import Event, Category, Organization

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'calendarapp/index.html'
    context_object_name = 'event_list'
    
    def get_queryset(self):
        return Event.objects.all()

class DetailView(generic.DetailView):
    model = Event
    template_name = 'calendarapp/detail.html'

class CalView(generic.ListView):
	template_name = 'calendarapp/cal.html'
	context_object_name = 'event_list'



