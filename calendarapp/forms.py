from django import forms
from .models import Event, Organization
from django.contrib.admin import widgets  
from django.forms import ModelForm
# from datetimewidget.widgets import DateTimeWidget


class AddEventForm(ModelForm):

	class Meta:
		model = Event
		fields = ('org', 'category', 'name', 'start_datetime', 'end_datetime', 'location', 'is_free', 'website', 'description',)
		# widgets = {
  #           'start_datetime': DateTimeWidget(attrs={'id':"start_datetime"}, usel10n = True, bootstrap_version=3),
  #           'end_datetime': DateTimeWidget(attrs={'id':"end_datetime"}, usel10n = True, bootstrap_version=3)
  #           }

	def __init__(self, *args, **kwargs):
		super(AddEventForm, self).__init__(*args, **kwargs)
		#self.fields['start_datetime'].widget = widgets.AdminSplitDateTime()
		# self.fields['end_datetime'].widget = widgets.AdminSplitDateTime()

class AddOrgForm(ModelForm):

	class Meta:
		model = Organization
		fields = ('name',)

	def __init__(self, *args, **kwargs):
		super(AddOrgForm, self).__init__(*args, **kwargs)

class FilterForm(forms.Form):
    locations = forms.CharField()
    is_free = forms.BooleanField()
    orgs = forms.CharField()



