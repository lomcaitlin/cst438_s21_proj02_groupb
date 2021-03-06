from django.urls import path

from django.contrin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]