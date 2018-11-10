from django.urls import path
from . import views

app_name = 'calendarapp'
urlpatterns = [
	path('', views.home, name='home'),
	path('addevent', views.AddEventView.as_view(), name='addevent'),
    path('cal', views.CalView.as_view(), name='cal'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail')
]
