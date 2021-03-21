from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from .models import URL, Item
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import UserUpdateForm, UserDeleteForm, ItemUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash, get_user_model


def index(request):
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
def new_item(request):
    form = ItemUpdateForm(request.POST or None)
    if form.is_valid():
    	# url = URL(url=request.cleaned_data.get('url_id'))
        form.save()# url.save()
        name=request.cleaned_data['name'],
        image=request.cleaned_data['image']
        description=request.cleaned_data['description']
        priority=request.cleaned_data['priority']
        user_id=get_user_model()
        url_id=request.cleaned_data['url_id']
        item = Item(
			name=name,
			image=image,
			description=description,
			priority=priority,
			user_id=user_id,
			url_id=url_id
            # name=request.cleaned_data['name'],
	        # image=request.cleaned_data['image'],
	        # description=request.cleaned_data['description'],
	        # priority=request.cleaned_data['priority'],
	        # user_id=get_user_model(),
	        # url_id=request.cleaned_data['url_id']
        )
        item.save()
        messages.success(request, "SUCCESSFULLY ADDED ITEM!")
        return HttpResponseRedirect('/index.html')
    else:
        messages.error(request, form.errors)
    return render(request, 'wishlistApp/newItem.html', {'form':form})
