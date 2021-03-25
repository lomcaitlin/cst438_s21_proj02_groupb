from django.test import TestCase
from .models import Item, URL
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your tests here.
class all_test(TestCase):
	def setup(self):
		user = User.objects.create_user('test', 'test@admin.com', 'password')
		user.save()
		temp = User.objects.create_user('temp', 'temp@aaa.com', 'password')
		temp.save()
		url = URL.objects.create(url='google.com')
		url.save()
		item = Item.objects.create(name='item1', image='image', description='description', priority=1, user_id=user, url_id=url)
		item.save()
	def test_user(self):
		print('running user test')
		self.setup()
		u = User.objects.all()
		self.assertEqual(len(u), 2)

	def test_url(self):
		print('running url test')
		self.setup()
		url = URL.objects.get(id=1)
		self.assertEqual(url.url, 'google.com')

	def test_item(self):
		print('running item test')
		self.setup()
		test_item = Item.objects.get(id=1)
		self.assertEqual(test_item.name, 'item1')

	def test_delete_user(self):
		print('running delete user')
		self.setup()
		temp = User.objects.get(id=2)
		temp.delete()
		self.assertEqual(len(User.objects.all()), 1) 
