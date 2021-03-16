from django.contrib import admin

# Register your models here.
from .models import URL, Item

admin.site.register(URL)
admin.site.register(Item)