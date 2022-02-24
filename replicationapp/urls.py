from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testing/', views.testing, name='testing'),
    path('department/', views.department, name='department'),
    path('event/', views.event, name='event'),
    path('instrument/', views.instrument, name='instrument'),
    path('instrument_group/', views.instrument_group, name='instrument_group'),
    path('synchronize/', views.synchronize, name='synchronize')
]