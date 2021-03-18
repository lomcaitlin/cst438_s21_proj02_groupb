from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from .models import URL, Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import UserUpdateForm, UserDeleteForm, ItemUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash, get_user_model


def index(request):
	if request.user.is_authenticated:
		allItems = request.user.item_set.all() # get all items by logged in user
		userItems = []
		priorityValue = request.GET.get('priority')
		keywordValue = request.GET.get('keyword')
		# if theres no query for anything, get all items
		if (priorityValue == "" and keywordValue == "" or (priorityValue==None and keywordValue==None)):
			userItems = allItems
		else:
			if priorityValue == "": #if priority value is nothing, only filter by keyword
				temp = allItems.filter(name__icontains=keywordValue)
			else: #filter by both keyword and priority
				temp = allItems.filter(priority=priorityValue, name__icontains=keywordValue)
			for i in temp:
				userItems.append(i)
		return render(request, 'wishlistApp/index.html', {'items':userItems})
	else:
		return render(request, 'wishlistApp/index.html')

@staff_member_required
def users(request):
	if request.method == 'POST':
		id = int(request.POST.get('deleteUser', ''))
		user = get_user_model().objects.get(pk=id)
		user.is_active = False
		user.save()
	context = {
		'users':  get_user_model().objects.all(),
		'title': 'View Users'
	}
	return render(request, 'wishlistApp/users.html', context)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}.')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'wishlistApp/register.html', {'form': form, 'title' : 'Register'})

@login_required
def profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, f"Your account has been updated.")
			return redirect('profile')
	else:
		form = UserUpdateForm(instance=request.user)
	return render(request, 'wishlistApp/profile.html', {'form' : form, 'title' : 'Profile'})

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, f"Your password has been updated.")
			return redirect('profile')
	else :
		form = PasswordChangeForm(request.user)
	return render(request, 'wishlistApp/change-password.html', {'form' : form, 'title' : 'Change Password'})

@login_required
def delete_account(request):
	if request.method == 'POST':
		form = UserDeleteForm(request.POST, instance=request.user)
		user = request.user
		user.delete()
		messages.success(request, f"Your account has been deleted.")
		return redirect('login')
	else:
		form = UserDeleteForm(instance=request.user)
	return render(request, 'wishlistApp/delete-account.html', {'form':form, 'title': 'Delete Account'})

@login_required
def user_list(request):
    user = request.user.get_username()
    return render(request, 'wishlistApp/userList.html', {'user':user})

@login_required
def filter(request):
	priority = request.GET.get('request')
	print(priority)
	return render(request, 'wishlistApp/index.html')

@login_required
def new_item(request):
    if request.method == 'POST':
        form = ItemUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            #grabbing info user typed in form to save into an Item obj
            #(not sure if saving the form OR putting info into an Item obj is correct)
            '''
            name = request.POST['itemN']
            itemURL = request.POST['itemURL']
            desc = request.POST['itemD']
            image = request.POST['imageURL']
            priority = request.POST['itemP']
            for urls in URL.objects.all():
                if urls == itemURL:
                    ins = Item(name=name, image=url, description=desc, priority = priority, user_id=request.user.get_username(), url_id=urls)
                    break
                else:
                    ins = Item(name=name, image=url, description=desc, priority = priority, user_id=request.user.get_username(), url_id=itemURL)
                    break
            ins.save()
            '''
            messages.success(request, f"Item has been added to your Wishlist!")
            return render(request, 'wishlistApp/newItem.html', {'form': form})
    else:
        form = ItemUpdateForm(request.POST, instance=request.user)
    return render(request, 'wishlistApp/newItem.html', {'form': form})
