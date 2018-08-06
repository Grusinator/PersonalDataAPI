from django.contrib import admin

# Register your models here.
from PersonalDataApi.profiles.models import Profile

admin.site.register(Profile)