import graphene
from graphene import AbstractType, Node, Mutation, String, ObjectType, Field, List, Date, Enum, Float

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphene_file_upload.scalars import Upload
from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from PersonalDataApi.users.schema import UserType

#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



from PersonalDataApi.datapoints.models import CategoryTypes, DatapointV2, MetaData, RawData
from PersonalDataApi.datapoints.schema_processing import ProcessRawData
from PersonalDataApi.users.models import Profile

from PersonalDataApi.services.google_speech_api import transcribe_file
#from PersonalDataApi.services.sound_processing_services import SoundClassifier

GrapheneCategoryTypes = Enum.from_enum(CategoryTypes)

class MetaDataType(DjangoObjectType):
    class Meta:
        model = MetaData

class DatapointType(DjangoObjectType):
    class Meta:
        model = DatapointV2
        # Allow for some more advanced filtering here
        #interfaces = (graphene.Node, )
        #filter_fields = {
        #    'name': ['exact', 'icontains', 'istartswith'],
        #    'notes': ['exact', 'icontains'],
        #}

class CreateDatapoint(graphene.Mutation):
    datapoint = Field(DatapointType)

    class Arguments:
        starttime = graphene.DateTime()
        endtime = graphene.DateTime()
        value = graphene.Float()
        std = graphene.Float()

        #meta params
        source = graphene.String()
        category = GrapheneCategoryTypes()
        label = graphene.String()

    @login_required
    def mutate(self, info, source, category, label, value, std,
               starttime, stoptime=None):

        try:
            metadata = MetaData.objects.get(
                source=source,
                category=category,
                label=label
                )
        except Exception as e:
            raise GraphQLError("no metadata object correspond to the combination of source, category and label")
            

        datapoint = DatapointV2(
            starttime=starttime,
            stoptime=stoptime,
            value=value,
            std=std,
            metadata=metadata,
            owner=info.context.user
            )

        datapoint.save()

        return CreateDatapoint(datapoint)

class RawDataType(DjangoObjectType):
    class Meta:
        model = RawData

class CreateRawData(graphene.Mutation):
    rawdata = Field(RawDataType)

    class Arguments:
        starttime = graphene.DateTime()
        stoptime = graphene.DateTime()
        files = Upload() #image and audio
        value = graphene.Float()
        std = graphene.Float()
        text = graphene.String()
        
        #meta params
        source = graphene.String()
        category = GrapheneCategoryTypes()
        label = graphene.String()



    @login_required
    def mutate(self, info, source, category, label, starttime, stoptime=None,
                value=None, std=None, text=None, files=None):

        metadata = MetaData.objects.get(
                source=source,
                category=category,
                label=label,
                raw=true
            )

        #Raw data should be processed into datapoints
        try:
            function = ProcessRawData.select_mutate_variant(self, category)

            datalist = function(self, info, source, category, label, starttime, stoptime=None,
                value=None, std=None, text=None, files=None)

            for data in datalist:
                if isinstance(DatapointV2):
                    data.save()
                elif isinstance(RawData):
                    data.metadata = metadata
                    data.save()
                    #make sure that the raw data is passed to response
                    rawdata = data
        except:
            pass
            print("eror occored while processing raw data..")

            rawdata = RawData(
                starttime=starttime,
                stoptime=stoptime,
                image=None,
                audio=None,
                value=value,
                std=std,
                text=text,
                metadata=metadata,
                owner=info.context.user
            )

            rawdata.save()

        return CreateRawData(rawdata=rawdata)


# test upload
class UploadFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # file parameter is key to uploaded file in FILES from context
        uploaded_file = info.context.FILES.get(file)
        # do something with your file

        return UploadFile(success=uploaded_file != None)

class Upload2Files(graphene.Mutation):
    class Arguments:
        files = Upload(required=True)


    success = graphene.Boolean()

    def mutate(self, info, files, **kwargs):
        # file parameter is key to uploaded file in FILES from context
        uploaded_file = info.context.FILES.get(files[0])
        uploaded_file = info.context.FILES["0"]
        uploaded_file2 = info.context.FILES.get(files[1])
        # do something with your file

        return UploadFile(success=uploaded_file != None)

# wrap all queries and mutations
class Query(graphene.ObjectType):
    datapoint = graphene.Field(DatapointType)
    all_rawdata = graphene.List(RawDataType)
    all_datapoints = graphene.List(DatapointType)

    @login_required
    def resolve_datapoint(self, info):

        datapoint = DatapointV2.objects.filter(owner=info.context.user).first()
        return datapoint

    @login_required
    def resolve_all_datapoints(self, info):
        datapointlist = DatapointV2.objects.filter(owner=info.context.user)
        return datapointlist

    @login_required
    def resolve_all_rawdata(self, info):
        datapointlist = RawData.objects.filter(owner=info.context.user)
        return datapointlist

class Mutation(graphene.ObjectType):
    create_datapoint = CreateDatapoint.Field()
    create_rawdata = CreateRawData.Field()
    upload_file = UploadFile.Field()
    upload2_files = Upload2Files.Field()
