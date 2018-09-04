from django.contrib import admin

# Register your models here.
from PersonalDataApi.datapoints.models import Datapoint, DatapointV2, MetaData, RawData

list = [Datapoint, DatapointV2, MetaData, RawData]
for model in list:
    admin.site.register(model)