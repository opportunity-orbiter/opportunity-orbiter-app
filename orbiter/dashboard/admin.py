from django.contrib import admin
from orbiter.dashboard.models import Company, Location, Job


# Register your models here.
admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Job)
