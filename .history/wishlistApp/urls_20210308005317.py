from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='wishlistApp/login.html'), name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('change-password/',
    #     auth_views.PasswordChangeView.as_view(
    #         template_name='wishlistApp/change-password.html',
    #         success_url='/profile'
    #     ),
    #     name='change-password'
    # ),
    path('change-password/', views.change_password, name='change-password'),
    path('delete-account/', views.delete_account, name='delete-account'),
    path('users/', views.users, name='view_users'),
]
