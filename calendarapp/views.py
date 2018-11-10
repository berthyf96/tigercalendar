#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse
from cas import CASClient
import os
import CASTest
from .forms import AddEventForm


from .models import Event, Category, Organization

# Create your views here.

def home(request):

	if request.GET.get('login'):
		print('hi')
		CASTest.test()

	return render(request, 'calendarapp/home.html', {})

class CalView(generic.ListView):
    template_name = 'calendarapp/index.html'
    context_object_name = 'event_list'
    
    def get_queryset(self):
        return Event.objects.all()

class DetailView(generic.DetailView):
    model = Event
    template_name = 'calendarapp/detail.html'

class AddEventView(generic.TemplateView):
	template_name = 'calendarapp/addevent.html'

	def get(self, request):
		form = AddEventForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = AddEventForm()
		if form.is_valid():
			post = form.save()
			name = form.cleaned_data['name']
			form = AddEventForm()
			return redirect(addevent)

		# args = {'form': form, 'name': name}
		return render(request, self.template_name, {'form': form})







