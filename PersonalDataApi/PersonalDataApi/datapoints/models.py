from django.db import models
from django.conf import settings

# Create your models here.

class Datapoint(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    category = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='datapoints/images', null=True, blank=True)
    audio = models.FileField(upload_to='datapoints/audio', null=True, blank=True)
    source_device = models.TextField(null=False, blank=False)
    value = models.FloatField(blank=True)
    text_from_audio = models.TextField(null=True,blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%i - %s - %s "%(self.id, self.category, self.source_device)

    class Meta:
        app_label = 'datapoints'