from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    admin = models.BooleanField(default=False)
    
class URL(models.Model):
    url = models.CharField(max_length=500)

class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    url_id = models.ForeignKey(URL, on_delete=models.CASCADE)


