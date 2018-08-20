from django.contrib import admin

# Register your models here.
from PersonalDataApi.users.models import Profile

admin.site.register(Profile)