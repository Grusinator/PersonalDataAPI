from django.contrib import admin

# Register your models here.
from PersonalDataApi.datapoints.models import Datapoint

admin.site.register(Datapoint)