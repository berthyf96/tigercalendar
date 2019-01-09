#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from CASClient import CASClient
from datetime import datetime
import json
import os
import CASTest
from .forms import AddEventForm, AddOrgForm
from .models import *
from dateutil.parser import parse
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import *

# Create your views here.
def home(request):

	if request.GET.get('login'):
		cas = CASClient(request)
		return cas.Authenticate()

	return render(request, 'calendarapp/home.html', {})

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

	eventsJson = serialize('json', event_list)
	eventsDict = json.loads(eventsJson)


	for i in range(len(eventsDict)):
		# Replace org ID with org name
		org_id = eventsDict[i]['fields']['org']
		if org_id is not None:
			org_name = Organization.objects.get(id=org_id).name
		eventsDict[i]['fields']['org'] = org_name

		# Replace category ID with category name
		categories = eventsDict[i]['fields']['category']
		category_names = []
		for j in range(len(categories)):
			category_name = Category.objects.get(id=categories[j]).name
			category_names.append(category_name)
		eventsDict[i]['fields']['category'] = category_names

	eventsJson = json.dumps(eventsDict)

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


@csrf_exempt
def createEvent(request):

	data = json.loads(request.body.decode('utf-8'))
	params = data['params']

	name = params['name']
	org_name = params['org']
	categories = params['cat']
	start = params['start_datetime']
	end = params['end_datetime']
	location = params['location']
	website = params['website']
	description = params['description']
	free = params['is_free']
	email = params['email']

	# Parse start and end date/times to the right format
	start_datetime = parse(start)
	end_datetime = parse(end)

	existing_events = Event.objects.filter(name__exact=name, start_datetime__exact=start_datetime)

	if (existing_events.count() > 0) :
		return HttpResponse('Duplicate event')

	# Get organizations from names
	orgs = Organization.objects.filter(name__exact=org_name)
	org = orgs[0] # Should only be one organization with that name

	# Parse category string into an array, then get the relevant category
	# objects
	cats = Category.objects.filter(name__in=categories)

	# Convert string to boolean
	if free == 'No': is_free = False
	else: is_free = True

	# Check to see if the event exists already
	# Defined by if there is an event with the same name/start time
	potential_event = Event.objects.filter(name__exact = name,
		start_datetime__exact=start_datetime)

	if potential_event.count() > 0:
		return HttpResponse('Event exists')

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
	e.save()

	# Get user
	users = User.objects.filter(email__exact=email)
	user = users[0]

	user.my_events.add(e)

	return HttpResponse('Created event')

@csrf_exempt
def createOrganization(request):

	data = json.loads(request.body.decode('utf-8'))
	params = data['params']
	name = params['name']
	email = params['email']

	existing_orgs = Organization.objects.filter(name__exact=name)

	if (existing_orgs.count() == 0) :
		o = Organization(name=name)
		o.save()

		# Get user
		users = User.objects.filter(email__exact=email)
		user = users[0]

		user.my_orgs.add(o)

		return HttpResponse('Created organization')
	else:
		return HttpResponse('Duplicate organization')

def deleteEvent(request):

	data = json.loads(request.body.decode('utf-8'))
	params = data['params']

	name = params['name']
	start = params['start_datetime']
	start_datetime = parse(start)

	events = Event.objects.filter(name__exact = name,
		start_datetime__exact = start_datetime)

	for e in events:
		e.delete()

	return HttpResponse('Success')

@csrf_exempt
def addUser(request):

	data = json.loads(request.body.decode('utf-8'))
	params = data['params']

	first_name = params['first_name']
	last_name = params['last_name']
	email = params['email']
	password = params['password']

	existing_users = User.objects.filter(email__exact=email)

	if (existing_users.count() > 0):
		return HttpResponse('Duplicate user')

	pw_encoded = make_password(password)

	admin = False

	u = User(first_name=first_name, last_name=last_name, email=email, \
		password = pw_encoded, admin = admin)
	u.save()

	return HttpResponse('Created user')

@csrf_exempt
def authenticateUser(request):

	data = json.loads(request.body.decode('utf-8'))
	params = data['params']

	email = params['email']
	password = params['password']

	users = User.objects.filter(email__exact=email)
	user = users[0]

	pw_encoded = user.password

	correct = check_password(password, pw_encoded)

	if correct == False:
		return HttpResponse('False')
	else:
		if user.admin == True:
			return HttpResponse('Admin')
		else:
			return HttpResponse('Not Admin')

@csrf_exempt
def checkAdminEvent(request):

	data = json.loads(request.body.decode('utf-8'))
	params = data['params']

	email = params['email']
	name = params['name']
	start = params['start_datetime']

	start_datetime = parse(start)

	users = User.objects.filter(email__exact=email)
	user = users[0]

	if user.admin == False:
		return HttpResponse('False')

	events = user.my_events

	if events.filter(name__exact = name, start_datetime = start_datetime) > 0:
		return HttpResponse('True')

	return HttpResponse('False')
