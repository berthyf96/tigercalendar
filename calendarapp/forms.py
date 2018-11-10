from django import forms
from .models import Event

class AddEventForm(forms.ModelForm):
	name = forms.CharField()

	class Meta:
		model = Event
		fields = ('org', 'category', 'name', 'start_datetime', 'end_datetime', 'location', 'is_free', 'website', 'description',)