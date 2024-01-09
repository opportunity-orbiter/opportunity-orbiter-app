from django.contrib import admin

from orbiter.laboratory.models import Webpage
from orbiter.laboratory.models import ToDoList
from orbiter.laboratory.models import ToDoItem

# Register your models here.
admin.site.register(Webpage)
admin.site.register(ToDoList)
admin.site.register(ToDoItem)
