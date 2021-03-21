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
        fields = [
            'name',
            'image',
            'description',
            'url_id',
            'priority',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ex. New Prebuilt PC!', 'label':'name'}),
            'image': forms.TextInput(attrs={'placeholder': 'Enter the image URL of the item', 'label':'image'}),
            'description': forms.TextInput(attrs={'placeholder': 'ex. New Prebuilt PC!', 'label':'description'}),
            'url_id': forms.TextInput(attrs={'placeholder': 'Enter the URL for the item', 'label':'url_id'}),
            'priority': forms.NumberInput(attrs={'label':'prio'}),
        }
