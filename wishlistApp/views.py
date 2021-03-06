from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from .models import URL, Item
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import UserUpdateForm, UserDeleteForm, ItemUpdateForm, ItemDeleteForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, ItemSerializer, UrlSerializer
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	if request.user.is_authenticated:
		clearSearch = False
		allItems = request.user.item_set.all() # get all items by logged in user
		userItems = []
		priorityValue = request.GET.get('priority')
		keywordValue = request.GET.get('keyword')
		# if theres no query for anything, get all items
		if (priorityValue == "" and keywordValue == "" or (priorityValue==None and keywordValue==None)):
			userItems = allItems
		else:
			clearSearch = True
			if priorityValue == "": #if priority value is nothing, only filter by keyword
				temp = allItems.filter(name__icontains=keywordValue)
			else: #filter by both keyword and priority
				temp = allItems.filter(priority=priorityValue, name__icontains=keywordValue)
			for i in temp:
				userItems.append(i)
		return render(request, 'wishlistApp/index.html', {'stuff':userItems, 'clearSearch':clearSearch})
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
def new_item(request):
    form = ItemUpdateForm(request.POST or None)
    if form.is_valid():
        name=form.cleaned_data['name']
        image=form.cleaned_data['image']
        description=form.cleaned_data['description']
        priority=form.cleaned_data['priority']
        user=request.user
        url=str(request.POST.get('iURL'))

		#saving URL
        if URL.objects.filter(url=url).exists():
            new_url = URL.objects.get(url=url)
            #new_url.save()
        else:
            new_url = URL(url=url)
            new_url.save()

		#saving Item
        item = Item(
			name=name,
			image=image,
			description=description,
			priority=priority,
			user_id=user,
			url_id=new_url
        )

        item.save()
        messages.success(request, f'SUCCESSFULLY ADDED {item.name}!')
        return HttpResponseRedirect('/')
    else:
        form = ItemUpdateForm(request.POST, instance=request.user)
        print("form not valid for soem reason")
    return render(request, 'wishlistApp/newItem.html', {'form': form, 'title': 'Add a new Item'})

@login_required
def update_items(request, pk):
    instance = Item.objects.get(id=pk)
    url_instance = instance.url_id.url
    form = ItemUpdateForm(request.POST or None, instance = instance)
    if form.is_valid():
        name=form.cleaned_data['name']
        image=form.cleaned_data['image']
        description=form.cleaned_data['description']
        priority=form.cleaned_data['priority']
        user=request.user
        url=str(request.POST.get('iURL'))

        if URL.objects.filter(url=url).exists():
            new_url = URL.objects.get(url=url)
            #new_url.save()
        else:
            new_url = URL(url=url)
            new_url.save()

        instance.name=name
        instance.image=image
        instance.description=description
        instance.priority=priority
        instance.url_id=new_url
        
        instance.save()
        messages.success(request, f'SUCCESSFULLY UPDATED {instance.name}!')
        return HttpResponseRedirect('/')
    return render(request, 'wishlistApp/update-item.html', {'form': form, 'title': 'Edit Item', 'url': url_instance})

@login_required
def delete_items(request,pk):
    instance = Item.objects.get(id=pk)
    if request.method == 'POST':
        form = ItemDeleteForm(request.POST or None, instance = instance)
        instance.delete()
        messages.success(request, f'SUCCESSFULLY DELETED ITEM FROM WISHLIST!')
        return HttpResponseRedirect('/')
    else:
        form = ItemDeleteForm(instance = instance)
    return render(request, 'wishlistApp/delete-item.html',{'form':form, 'title': 'Delete Item', 'item': instance.name})

@api_view(['GET'])
def api_overview(request):
	api_urls = {
		'View user': '/user/',
		'View user by id': '/user/<str:pk>',
		'Create user': '/create-user/',
		'Update user': '/update-user/<str:pk>',
		'Delete user': '/delete-user/<str:pk>',
		'View items': '/item/',
		'View items by user id': 'item/user_id/<str:user_id>',
		'View items by id':'item/<str:pk>',
		'Update item': 'update-item/<str:pk>',
		'Create item': '/create-item/',
		'Delete item': '/delete-item/<str:pk>',
		'View URL': '/url/',
		'View URL by id': '/url/<str:pk>',
		'Create URL': '/create-url/',
		'Update URL': '/update-url/<str:pk>',
		'Delete URL': '/delete-url/<str:pk>',
	}
	return Response(api_urls)

@api_view(['GET'])
def view_users(request):
	users = get_user_model().objects.all()
	serializer = UserSerializer(users, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def view_user(request, pk):
	users = get_user_model().objects.get(id=pk)
	serializer = UserSerializer(users, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def update_user(request, pk):
	user = get_user_model().objects.get(id=pk)
	serializer = UserSerializer(instance = user, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(request, pk):
	user = get_user_model().objects.get(id=pk)
	user.delete()
	return Response("User deleted")

@api_view(['GET'])
def view_items(request):
	items = Item.objects.all()
	serializer = ItemSerializer(items, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def view_items_by_user(request, id):
	try:
		items = Item.objects.filter(user_id=id)
	except Item.DoesNotExist:
		return HttpResponse("ID not found or something")
	serializer = ItemSerializer(items, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def view_items_by_id(request, pk):
	try:
		items = Item.objects.get(id=pk)
	except Item.DoesNotExist:
		return HttpResponse("ID not found or something")
	serializer = ItemSerializer(items, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def create_item(request):
	serializer = ItemSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['DELETE'])
def delete_item(request, pk):
	item = Item.objects.get(id=pk)
	item.delete()
	return Response("Item deleted")

@api_view(['POST'])
def update_item(request, pk):
	try:
		item = Item.objects.get(id=pk)
	except Item.DoesNotExist:
		return HttpResponse("ID not found or something")
	serializer = ItemSerializer(instance = item, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['GET'])
def view_url(request):
	url = URL.objects.all()
	serializer = UrlSerializer(url, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def view_url_by_id(request, pk):
	try:
		url = URL.objects.get(id=pk)
	except URL.DoesNotExist:
		return HttpResponse("ID not found or something")
	serializer = UrlSerializer(url, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def create_url(request):
	serializer = UrlSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['DELETE'])
def delete_url(request, pk):
	url = URL.objects.get(id=pk)
	url.delete()
	return Response("URL deleted")

@api_view(['POST'])
def update_url(request, pk):
	try:
		url = URL.objects.get(id=pk)
	except URL.DoesNotExist:
		return HttpResponse("ID not found or something")
	serializer = UrlSerializer(instance = url, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)
