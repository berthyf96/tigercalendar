#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.core.serializers import serialize
from CASClient import CASClient
from datetime import datetime
import json
import os
import CASTest
from .forms import AddEventForm, AddOrgForm
from .models import *
from dateutil.parser import parse
from django.views.generic.edit import CreateView

# Create your views here.
def home(request):

	if request.GET.get('login'):
		cas = CASClient(request)
		return cas.Authenticate()

	return render(request, 'calendarapp/home.html', {})

def login(request):
    cas = CASClient(request)
    return cas.Authenticate()

def netid(request):
	# cas = CASClient(request)
	# netid = cas.Validate(request.GET.get('ticket'))
	# if netid == None:
	# 	return HttpResponse("-")
	# else:
	# 	return HttpResponse(netid)
	netid = request.session.get('netid')
	return render(request, 'calendarapp/netid.html', {'netid': netid})

# Return name of organization given ID.
def getOrgName(request, orgPk):
    org = [Organization.objects.get(pk=orgPk)]
    json = serialize('json', org)
    data = {'data': json}
    return JsonResponse(data)


## THIS FILTERS THE EVENTS FOR LOCATIONS, FREE BOOLEAN, AND ORGANIZATIONS
def getEvents(request):

	locations_list = None
	categories_list = None
	org_list = None
	is_free = None
	start_date = None
	end_date = None
	netid = None
	favorites = None

	# comma-deliminated string with list of locations
	locations = request.GET.get('locations')
	if locations and locations != "":
		locations_list = locations.split(',')
	# comma-deliminated string with list of categories
	categories = request.GET.get('categories')
	if categories and categories != "":
		categories_list = categories.split(',')
	# comma-deliminated string with list of orgs
	orgs = request.GET.get('organizations')
	if orgs and orgs != "":
		org_list = orgs.split(',')
	# should be either empty string or 'true'
	is_free = request.GET.get('is_free')
	if is_free and is_free != "":
		is_free = request.GET.get('is_free')
	# comma-deliminated string containing date (Y,M,D), i.e. '2018,12,4'
	start_date_request = request.GET.get('start_date')
	if start_date_request and start_date_request != "":
		start_date_list = start_date_request.split(',')
		if len(start_date_list) == 3:
			start_date = datetime.date(start_date_list[0],
										start_date_list[1], start_date_list[2])
	# comma-deliminated string containing date (Y,M,D), i.e. '2018,12,4'
	end_date_request = request.GET.get('end_date')
	if (end_date_request and end_date_request != ""):
		end_date_list = end_date_request.split(',')
		if len(end_date_list) == 3:
			end_date = datetime.date(end_date_list[0], end_date_list[1],
										end_date_list[2])

	# Need to get the netid of the user
	netid = request.GET.get('netid')

	# should be either empty string or 'true'
	favorites = request.GET.get('favorites')
	if favorites and favorites != "":
		favorites = request.GET.get('favorites')

	event_list = filterEvents(locations_list=locations_list, categories_list=categories_list,
								org_list=org_list, is_free=is_free, start_date=start_date,
								end_date=end_date, netid = netid, favorites = favorites)
	#print(event_list)

	eventsJson = serialize('json', event_list)
	# eventsJson = json.loads(eventsJson)

	# for i in range(0, len(eventsJson)):
	# 	# Should return org names, not org id's!
	# 	org_id = eventsJson[i]['fields']['org']
	# 	eventsJson[i]['fields']['org'] = Organization.objects.get(id=org_id).name
	#
	# 	# Should return category names, not category id's!
	# 	categories = eventsJson[i]['fields']['category']
	# 	for j in range(0, len(categories)):
	# 		categories[j] = Category.objects.get(id=categories[j]).name

	data = {'Events_JSON': eventsJson}
	return JsonResponse(data)

# return list of filtered events based on parameters
def filterEvents(locations_list=None, categories_list=None, org_list=None,
					is_free=None, start_date=None, end_date=None,
					netid = None, favorites=None):

	event_list = Event.objects.all()

	if (favorites and favorites == "true"):

		# Find user
		user = User.objects.filter(netid__exact = netid)
		if len(user) == 1:

			# Turn list into just the one user
			user = user[0]
			event_list = user.favorite_events.all()

			# Do we need to add a corner case for if the user has no
			# favorites?

	if (locations_list):
		event_list = event_list.filter(location__in=locations_list)
	if (categories_list):
		event_list = event_list.filter(category__name__in=categories_list)
	if (org_list):
		event_list = event_list.filter(org__name__in=org_list)
	if (is_free and is_free == "true"):
		event_list = event_list.filter(is_free__exact="True")
	if (start_date and end_date):
		event_list = event_list.filter(start_datetime__range=(start_date, end_date))

	return event_list

# return all organization names
def getOrganizations(request):
	org_names = Organization.objects.all().values_list('name', flat=True).distinct()
	org_names = [org for org in org_names if org is not None]
	return JsonResponse({'orgs':org_names})

# return all location names
def getLocations(request):
	locations = Event.objects.all().values_list('location', flat = True).distinct()
	locations = [loc for loc in locations if loc is not None]
	return JsonResponse({'locs':locations})

# return all categories
def getCategories(request):
	cat_names = Category.objects.all().values_list('name', flat = True).distinct()
	cat_names = [cat for cat in cat_names if cat is not None]
	return JsonResponse({'cats':cat_names})

# Add a user favorite
# Takes in a string (user)
# Another string (name)
# Start date and time (start_datetime)
def addFavorite(request):
	netid = request.GET.get('user')
	if netid is None:
		netid = 'rb25'

	name = request.GET.get('name')

	# Need to parse the start time like we did in the form
	# Takes in the form Thu, 27 Dec 2018 05:00:00 GMT
	start = request.GET.get('start_datetime')
	start_datetime = parse(start)

	event_set = Event.objects.filter(name__exact = name).filter(start_datetime__exact = start_datetime)
	if len(event_set) != 1: return HttpResponse("failed")

	event = event_set[0]

	# User does not already exists...
	if not User.objects.filter(netid = netid).exists():
		new_user = User(netid = netid)
		new_user.save()

	# Now that user exists, add event to user favorites
	user = User.objects.filter(netid = netid)
	if len(user) != 1: return HttpResponse("failed")

	# Turn list into just the one user
	user = user[0]

	# Now save the designated event to their favorites
	user.favorite_events.add(event)
	return HttpResponse("success")

def createEvent(request):

	name = None
	org_name = None
	cat = None
	start_datetime = None
	end_datetime = None
	location = None
	website = None
	description = None
	is_free = None

	# comma-deliminated string with list of locations
	name = request.GET.get('name')
	org_name = request.GET.get('org')
	cat_names = request.GET.get('cat')
	start = request.GET.get('start_datetime')
	end = request.GET.get('end_datetime')
	location = request.GET.get('location')
	website = request.GET.get('website')
	description = request.GET.get('description')
	free = request.GET.get('is_free')

	# Get organizations from names
	orgs = Organization.objects.filter(name__exact=org_name)
	org = orgs[0] # Should only be one organization with that name

	# Parse category string into an array, then get the relevant category
	# objects
	cat_names_array = cat_names.split(',')
	cats = Category.objects.filter(name__in = cat_names_array)

	# Parse start and end date/times to the right format
	start_datetime = parse(start)
	end_datetime = parse(end)

	# Convert string to boolean
	if free == 'No': is_free = False
	else: is_free = True

	e = Event(org=org, name=name, start_datetime=start_datetime, \
		end_datetime=end_datetime, is_free=is_free)
	e.save()

	e.category.set(cats) # Must set many-to-many field after the fact

	# Set non-required categories if they exist
	if location != '':
		e.location = location
	if description != '':
		e.description = description
	if website != '':
		e.website = website

def createOrganization(request):

	name = None
	name = request.GET.get('name')

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

# class AppointmentCreateView(CreateView):
#     """Powers a form to create a new appointment"""

#     model = Appointment
#     fields = ['name', 'phone_number', 'time']
