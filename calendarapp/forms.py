from django import forms
from .models import Event
from django.contrib.admin import widgets  


class AddEventForm(forms.ModelForm):
	# org = forms.ForeignKey()
	# category = forms.CharField()
	# name = forms.CharField()
	#start_datetime = forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])
	#end_datetime = forms.DateTimeField()
	# end_datetime = forms.DateTimeField()
	# location = forms.CharField()
	# is_free = forms.BooleanField()
	# website = forms.CharField()
	# description = forms.CharField()

	class Meta:
		model = Event
		fields = ('org', 'category', 'name', 'start_datetime', 'end_datetime', 'location', 'is_free', 'website', 'description',)

	def __init__(self, *args, **kwargs):
		super(AddEventForm, self).__init__(*args, **kwargs)
		self.fields['start_datetime'].widget = widgets.AdminSplitDateTime()
		self.fields['end_datetime'].widget = widgets.AdminSplitDateTime()
