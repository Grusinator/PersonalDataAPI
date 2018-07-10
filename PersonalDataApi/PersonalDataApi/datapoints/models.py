from django.db import models
from django.conf import settings

# Create your models here.

class Datapoint(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True,blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'datapoints'