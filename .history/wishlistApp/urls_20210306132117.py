from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views as 


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.index, name='login'),
    path('logout/', views.index, name='logout'),
    
]