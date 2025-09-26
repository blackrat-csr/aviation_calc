from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.home, name='home'),
    path('wind-triangle/', views.wind_triangle, name='wind_triangle'),
    path('great-circle/', views.great_circle, name='great_circle'),
    path('rhumb-line/', views.rhumb_line, name='rhumb_line'),
    path('history/', views.history, name='history'),
]