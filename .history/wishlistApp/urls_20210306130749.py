from django.urls import path

from django.contrib.auth import

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]