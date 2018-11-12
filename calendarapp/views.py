#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.core.serializers import serialize
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

def getEvents(request):
    eventsJson = serialize('json', Event.objects.all())
    data = {'Events_JSON': eventsJson}
    return JsonResponse(data)

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
		form = AddEventForm(request.POST)
		if form.is_valid():
			print('valid')
			post = form.save()
			form = AddEventForm()
			return redirect(addevent)
		else: 
			print('errors')
			print(form.errors)

		# org = form.cleaned_data['org']
			# category = form.cleaned_data['category']
			# name = form.cleaned_data['name']
			# start_datetime = form.cleaned_data['start_datetime']
			# end_datetime = form.cleaned_data['end_datetime']
			# location = form.cleaned_data['location']
			# is_free = form.cleaned_data['is_free']
			# website = form.cleaned_data['website']
			# description = form.cleaned_data['description']

		

			#args = {'form': form, 'name': name}
		args = {'form': form}
		return render(request, self.template_name, args)







