from django.urls import path

from django

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]