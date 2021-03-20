from rest_framework import serializers
from .models import URL, Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'

class UrlSerializer(serializers.ModelSerializer):
	class Meta:
		model = URL
		fields = '__all__'