from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views as user_views


urlpatterns = [
    path('', user_views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name=''), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]