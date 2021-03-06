from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views as user_views


urlpatterns = [
    path('', user_views.index, name='index'),
    path('login/', auth_views.loginView.as_view(), name='login'),
    path('logout/', auth_views.index, name='logout'),
    
]