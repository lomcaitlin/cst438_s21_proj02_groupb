from django.urls import path

from 

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]