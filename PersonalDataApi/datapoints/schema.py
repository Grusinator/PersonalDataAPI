import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphene_file_upload import Upload

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from PersonalDataApi.users.schema import UserType
from django.contrib.auth import get_user_model

from PersonalDataApi.datapoints.models import Datapoint, CategoryTypes
from PersonalDataApi.profiles.models import Profile

from PersonalDataApi.services.google_speech_api import transcribe_file

GrapheneCategoryTypes = graphene.Enum.from_enum(CategoryTypes)

class DatapointType(DjangoObjectType):
    class Meta:
        model = Datapoint
        # Allow for some more advanced filtering here
        #interfaces = (graphene.Node, )
        #filter_fields = {
        #    'name': ['exact', 'icontains', 'istartswith'],
        #    'notes': ['exact', 'icontains'],
        #}

class CreateDatapoint(graphene.Mutation):
    id = graphene.Int()
    datetime = graphene.DateTime()
    category = GrapheneCategoryTypes()
    source_device = graphene.String()
    value = graphene.Float()
    text_from_audio = graphene.String()
    owner = graphene.Field(UserType)
    source_device = graphene.String()
    value = graphene.Float()
    text_from_audio = graphene.String()

    class Arguments:
        datetime = graphene.DateTime()
        category = GrapheneCategoryTypes()
        source_device = graphene.String()
        value = graphene.Float()
        text_from_audio = graphene.String()
        files = Upload()


    @login_required
    def mutate(self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):

        uploaded_image = uploaded_audio = None

        if files != None:
            #make sure which one is the image, audio
            # currently we are assuming the first one is image, the second audio
            uploaded_image = info.context.FILES.get(files[0])
            uploaded_audio = info.context.FILES.get(files[1])

   
        profile = Profile.objects.get(user=info.context.user)
        

        try:
            text_from_audio = transcribe_file(uploaded_audio, profile.language) if (uploaded_audio != None) else None 
        except ValueError as e:
            print(e)

        datapoint = Datapoint(
            datetime=datetime,
            category=category,
            image=uploaded_image,
            audio=uploaded_audio,
            source_device=source_device,
            value=value,
            text_from_audio=text_from_audio,
            owner=info.context.user,
        )
        datapoint.save()

        return CreateDatapoint(
            id=datapoint.id,
            datetime=datapoint.datetime,
            category=datapoint.category,
            source_device=datapoint.source_device,
            value=datapoint.value,
            text_from_audio=datapoint.text_from_audio,
            owner=datapoint.owner,
        )

class DeleteDatapoint(graphene.Mutation):
    id = graphene.Int()
    owner = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int()

    @login_required
    def mutate(self, info, id):
        try:
            datapoint = Datapoint.objects.get(id=id, owner=info.context.user)
        except:
            raise GraphQLError('that datapoint id does not exist, or you do not own it')

        datapoint.delete()
        return CreateDatapoint(
            id=datapoint.id,
            owner=datapoint.owner
        )

class EditDatapoint(graphene.Mutation):
    id = graphene.Int()
    owner = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int()

    @login_required
    def mutate(self, info, id, name=None, notes=None):
        try:
            datapoint = Datapoint.objects.get(id=id, owner=info.context.user) 
        except:
            raise GraphQLError("datapoint does not exist, or you dont own this datapoint")

        #update each attribute
        if name is not None:
            datapoint.name=name
        if notes is not None:
            datapoint.notes=notes
        datapoint.save()

        return CreateDatapoint(
            id=datapoint.id,
            name=datapoint.name,
            notes=datapoint.notes,
            owner=datapoint.owner
        )


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
        uploaded_file2 = info.context.FILES.get(files[1])
        # do something with your file

        return UploadFile(success=uploaded_file != None)

class Query(graphene.ObjectType):
    datapoint = graphene.Field(DatapointType)
    all_datapoints = graphene.List(DatapointType)

    @login_required
    def resolve_datapoint(self, info):

        datapoint = Datapoint.objects.filter(owner=info.context.user).first()
        return datapoint

    @login_required
    def resolve_all_datapoints(self, info):

        datapointlist = Datapoint.objects.filter(owner=info.context.user)
        return datapointlist

class Mutation(graphene.ObjectType):
    create_datapoint = CreateDatapoint.Field()
    edit_datapoint = EditDatapoint.Field()
    delete_datapoint = DeleteDatapoint.Field()
    upload_file = UploadFile.Field()
    upload2_files = Upload2Files.Field()
