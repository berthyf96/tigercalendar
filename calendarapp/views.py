#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.core.serializers import serialize
from CASClient import CASClient
import json
import os
import CASTest
from .forms import AddEventForm, AddOrgForm
from .models import Event, Category, Organization

# Create your views here.
def home(request):

	if request.GET.get('login'):
		cas = CASClient(request)
		return cas.Authenticate()

	return render(request, 'calendarapp/home.html', {})

def login(request):
    cas = CASClient(request)
    return cas.Authenticate()

# class FormView(generic.TemplateView):
# 	template_name = 'calendarapp/form.html'
#
# 	def get(self, request):
# 		form = FilterForm()
# 		return render(request, self.template_name, {'form': form})
#
# 	def post(self, request):
#
# 		form = FilterForm(request.POST)
#
# 		if form.is_valid():
# 			locations = form.cleaned_data['locations']
# 			is_free = form.cleaned_data['is_free']
# 		else:
# 			print('errors')
# 			print(form.errors)
#
# 		context={
#     		'form': form,
#     		'locations': locations,
# 	    	'is_free': is_free,
# 		}
# 		return redirect('calendarapp:filter', context)

# Return name of organization given ID.
def getOrgName(request, orgPk):
    org = [Organization.objects.get(pk=orgPk)]
    json = serialize('json', org)
    data = {'data': json}
    return JsonResponse(data)


## THIS FILTERS THE EVENTS FOR LOCATIONS, FREE BOOLEAN, AND ORGANIZATIONS
def getEvents(request):
	event_list = Event.objects.all()
	locations_list = None
	categories_list = None
	is_free = None

	locations = request.GET.get('locations') # is a string
	if locations and locations != "":
		locations_list = locations.split(',')

	categories = request.GET.get('categories')
	if categories and categories != "":
		categories_list = categories.split(',')

	is_free = request.GET.get('is_free')
	if is_free and is_free != "":
		is_free = request.GET.get('is_free')

	if (locations_list):
		event_list = event_list.filter(location__in=locations_list)
	if (categories_list):
		event_list = event_list.filter(category__in=categories_list)
	if (is_free and is_free == "true"):
		event_list = event_list.filter(is_free__exact="True")

	print(event_list)

	eventsJson = serialize('json', event_list)
	eventsJson = json.loads(eventsJson)

	for i in range(0, len(eventsJson)):
		# Should return org names, not org id's!
		org_id = eventsJson[i]['fields']['org']
		eventsJson[i]['fields']['org'] = Organization.objects.get(id=org_id).name

		# Should return category names, not category id's!
		categories = eventsJson[i]['fields']['category']
		for j in range(0, len(categories)):
			categories[j] = Category.objects.get(id=categories[j]).name

	data = {'Events_JSON': eventsJson}
	return JsonResponse(data)

# return all organization names
def getOrganizationNames(request):
	org_names = Organization.objects.all().values_list('name', flat=True).distinct()
	org_names = [org for org in org_names if org is not None]
	orgNamesJson = serialize('json', org_names)
	data = {'OrgNames_JSON': orgNamesJson}
	return JsonResponse(data)

# return all location names
def getLocations(request):
	locations = Event.objects.all().values_list('location', flat = True).distinct()
	locations = [loc for loc in locations if loc is not None]
	locJson = serialize('json', locations)
	data = {'Location_JSON': locJson}
	return JsonResponse(data)

# return all categories
def getCategories(request):
	cat_names = Category.objects.all().values_list('name', flat = True).distinct()
	cat_names = [cat for cat in cat_names if cat is not None]
	catJson = serialize('json', cat_names)
	data = {'Category_JSON': catJson}
	return JsonResponse(data)


def createEvent(org, cat, name, start_datetime, end_datetime, location, is_free, website, description):
	e = Event(org=org, category=cat, name=name, start_datetime=start_datetime, \
		end_datetime=end_datetime, location=location, is_free=is_free, website=website, \
		description=description)
	e.save()

def createOrganization(name):
	o = Organization(name=name)
	o.save()

class CalView(generic.ListView):
    template_name = 'calendarapp/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.all()

class FilterView(generic.ListView):
    template_name = 'calendarapp/filter.html'
    context_object_name = 'event_list'

    def get_queryset(self):
    	locations=['Baker Rink']
    	is_free=False
    	orgs=['PUFSC']
    	event_list = Event.objects.filter(location__in=locations, is_free__exact=is_free,org__name__in=orgs)
    	return event_list
    	#return Event.objects.all()


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
			form.save()
			form = AddEventForm()
			return redirect('calendarapp:addevent')
		else:
			print('errors')
			print(form.errors)


		args = {'form': form}
		return render(request, self.template_name, args)

class AddOrgView(generic.TemplateView):
	template_name = 'calendarapp/addorg.html'

	def get(self, request):
		form = AddOrgForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request):

		form = AddOrgForm(request.POST)

		if form.is_valid():
			print('valid')
			form.save()
			form = AddOrgForm()
			return redirect('calendarapp:addorg')
		else:
			print('errors')
			print(form.errors)

		args = {'form': form}
		return render(request, self.template_name, args)
