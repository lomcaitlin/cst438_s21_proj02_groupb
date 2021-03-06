from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from .models import User, URL, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def index(request):
    return render(request, 'wishlistApp/index.html')

def users(request):
	context = {
		'users': User.objects.all()
	}
	return render(request, 'wishlistApp/users.html', context)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}.')
			return redirect('index')
	else:
		form = UserCreationForm()
	return render(request, 'wishlistApp/register.html', {'form': form, 'title' : 'Register'})
