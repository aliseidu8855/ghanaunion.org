
from django.urls import path
from . import views

app_name = 'events'


urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/rsvp/', views.event_rsvp_view, name='rsvp'),
]