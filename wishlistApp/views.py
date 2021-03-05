from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from .models import User, URL, Item

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def users(request):
	context = {
		'users': User.objects.all()
	}
	return render(request, 'wishlistApp/users.html', context)