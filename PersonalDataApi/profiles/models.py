from django.db import models
from django.conf import settings
from enum import Enum

# Create your models here.


class Languages(Enum):
    Danish = "dk"
    English = "en"

class Profile(models.Model):
    name = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    language = models.TextField(null=False, blank=False, max_length=2,
        choices=[(tag.value, tag.name) for tag in Languages])
    profilepicture = models.ImageField(upload_to='profilepictures', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%i - %s - %s - %s"%(self.id, self.user.username, self.name, self.language)

    class Meta:
        app_label = 'profiles'