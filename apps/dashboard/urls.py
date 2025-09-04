from django.urls import path
from .views import analytics_dashboard_view

app_name = 'dashboard'

urlpatterns = [
    path('analytics/', analytics_dashboard_view, name='analytics'),
]