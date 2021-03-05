from django.contrib import admin

# Register your models here.
from .models import User, URL, Item

admin.site.register(User)
admin.site.register(URL)
admin.site.register(Item)