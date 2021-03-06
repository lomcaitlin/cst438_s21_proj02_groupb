from django.urls import path

from django.contrib

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]