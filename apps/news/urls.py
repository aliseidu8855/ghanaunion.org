from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail'),
    path('tag/<str:tag_name>/', views.NewsListView.as_view(), name='list_by_tag'),
]