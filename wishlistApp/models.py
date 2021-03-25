from django.db import models
from django.conf import settings
# Create your models here.
"""
class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    admin = models.BooleanField(default=False)
"""

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class URL(models.Model):
    url = models.CharField(max_length=500)

class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    priority = IntegerRangeField(min_value=0, max_value=5)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url_id = models.ForeignKey(URL, on_delete=models.CASCADE)
