from django.urls import path
from . import views

app_name = 'calendarapp'
urlpatterns = [
	path('', views.home, name='home'),
	path('login', views.login, name='login'),
	path('addevent', views.AddEventView.as_view(), name='addevent'),
    path('netid', views.netid, name='netid'),
	#path('form', views.FormView.as_view(), name='form'),
	#path('filter', views.FilterView.as_view(), name='filter'),
	path('addorg', views.AddOrgView.as_view(), name='addorg'),
    path('cal', views.CalView.as_view(), name='cal'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('getOrgName/<int:orgPk>/', views.getOrgName, name='getOrgName'),
    path('getEvents', views.getEvents, name='getEvents'),
	path('getOrganizations', views.getOrganizations, name='getOrganizations'),
	path('getLocations', views.getLocations, name='getLocations'),
	path('getCategories', views.getCategories, name='getCategories'),
]
