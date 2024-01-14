from django.contrib import admin
from orbiter.dashboard.models import Webpage, Company, Location, Job


# Register your models here.
admin.site.register(Webpage)
admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Job)
