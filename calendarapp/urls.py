from django.urls import path
from . import views

app_name = 'calendarapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cal', views.CalView.as_view(), name='cal'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail')
]
