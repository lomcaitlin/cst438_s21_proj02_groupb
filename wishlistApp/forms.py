from django import forms
from django.contrib.auth.models import User
from .models import Item, URL

class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username']

class UserDeleteForm(forms.ModelForm):
  class Meta:
    model = User
    fields = []

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name","image","description","priority","url_id"]
