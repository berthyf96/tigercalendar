# import httplib2
# from googleapiclient.discovery import build
# from oauth2client.service_account import ServiceAccountCredentials
# from oauth2client import crypt

# service_account_email = 'whatsroaring18@whatsroaring.iam.gserviceaccount.com'

# CLIENT_SECRET_FILE = 'pem.p12'

# SCOPES = 'https://www.googleapis.com/auth/calendar'
# scopes = [SCOPES]

# from google.oauth2 import service_account
# import googleapiclient.discovery


SCOPES = ['https://www.googleapis.com/auth/calendar']
#SERVICE_ACCOUNT_FILE = 'whatsroaring1818_pem.p12'
SERVICE_ACCOUNT_FILE = 'whatsroaring1818_pem.json'
#SERVICE_KEY = AIzaSyBcQmNflSd-w_djdLAJDZclPj_ZG5NkbL4

# def build_service():

	# credentials = ServiceAccountCredentials.from_p12_keyfile(
	# 	service_account_email=service_account_email,
	# 	filename=CLIENT_SECRET_FILE,
	# 	scopes=SCOPES
	# )

	# http = credentials.authorize(httplib2.Http())

	# service = build('calendar', 'v3', http=http)

	# return service

# def exportToCalendar(request):

# 	# data = json.loads(request.body.decode('utf-8'))
# 	# params = data['params']

# 	# name = params['name']
# 	# start = params['start_datetime']
# 	# end = params['end_datetime']

# 	# # Parse start and end date/times to the right format
# 	# start_datetime = parse(start)
# 	# end_datetime = parse(end)

# 	# service = build_service()

# 	GMT_OFF = '-05:00'

# 	event = {
# 	  'summary': 'Dinner with friends',
# 	  'start': {'dateTime': '2019-01-07T09:00:00%s' % GMT_OFF},
# 	  'end': {'dateTime': '2019-01-07T11:00:00%s' % GMT_OFF},
# 	}

# 	# #event = service.events().insert(calendarId='beckybarber18@gmail.com', body=event).execute()
# 	# event = service.events().insert(calendarId='primary', body=event).execute()

# 	# print(event)

# 	# return HttpResponse('success')

# 	credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 	# http = httplib2.Http()
# 	# credentials.authorize(http)
# 	# if not credentials.access_token:
# 	#     credentials.refresh(http)

# 	service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

# 	# THIS GIVES AN ERROR
# 	# event = service.events().insert(calendarId='beckybarber18@gmail.com', body=event).execute()

# 	# THIS SUCCEEDS, BUT THE EVENT IS NOT ADDED TO A CALENDAR
# 	event = service.events().insert(calendarId='primary', body=event).execute()

# 	print(event)

# 	return HttpResponse('success')

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