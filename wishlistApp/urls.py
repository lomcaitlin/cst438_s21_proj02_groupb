from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='wishlistApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='wishlistApp/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('delete-account/', views.delete_account, name='delete-account'),
    path('users/', views.users, name='view_users'),
    path('add-item/', views.new_item, name='newItem'),
    path('api/', views.api_overview, name='api_overview'),
    path('api/user/', views.view_users, name='view_users'),
    path('api/user/<str:pk>/', views.view_user, name='view_user'),
    path('api/create-user/', views.create_user, name='create_user'),
    path('api/update-user/<str:pk>', views.update_user, name='update_user'),
    path('api/delete-user/<str:pk>', views.delete_user, name='delete_user'),
    path('api/item/', views.view_items, name='view_items'),
    path('api/item/user_id/<str:id>', views.view_items_by_user, name='view_items_by_user'),
    path('api/item/<str:pk>', views.view_items_by_id, name='view_items_by_id'),
    path('api/create-item/', views.create_item, name='create_item'),
    path('api/delete-item/<str:pk>', views.delete_item, name='delete_item'),
    path('api/update-item/<str:pk>', views.update_item, name='update_item'),
    path('api/url/', views.view_url, name='view_url'),
    path('api/url/<str:pk>', views.view_url_by_id, name='view_url_by_id'),
    path('api/create-url/', views.create_url, name='create_url'),
    path('api/delete-url/<str:pk>', views.delete_url, name='delete_url'),
    path('api/update-url/<str:pk>', views.update_url, name='update_url'),
]
