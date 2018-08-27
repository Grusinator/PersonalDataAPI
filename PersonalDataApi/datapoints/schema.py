import graphene
from graphene import AbstractType, Node, Mutation, String, ObjectType, Field, List, Date, Enum, Float

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphene_file_upload.scalars import Upload
from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from PersonalDataApi.users.schema import UserType

from django.contrib.auth import get_user_model



from PersonalDataApi.datapoints.models import Datapoint, CategoryTypes
from PersonalDataApi.users.models import Profile

from PersonalDataApi.services.google_speech_api import transcribe_file
#from PersonalDataApi.services.sound_processing_services import SoundClassifier

GrapheneCategoryTypes = Enum.from_enum(CategoryTypes)

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
    datapoint = Field(DatapointType)
    #id = graphene.Int()
    #datetime = graphene.DateTime()
    #category = GrapheneCategoryTypes()
    #source_device = graphene.String()
    #value = graphene.Float()
    #text_from_audio = graphene.String()
    #owner = graphene.Field(UserType)
    #source_device = graphene.String()
    #value = graphene.Float()
    #text_from_audio = graphene.String()

    class Arguments:
        datetime = graphene.DateTime()
        category = GrapheneCategoryTypes()
        source_device = graphene.String()
        value = graphene.Float()
        text_from_audio = graphene.String()
        files = Upload()

    def speech_audio(self, info, category, source_device,
            datetime=None, value=None, text_from_audio=None, files=None):

        uploaded_image = uploaded_audio = None

        if files != None:
            #make sure which one is the image, audio
            # currently we are assuming the first one is image, the second audio
            # uploaded_image = info.context.FILES.get(files[0])
            uploaded_audio = info.context.FILES["0"]

        valid_voice_list = ["Speech", "Dialog", "Laughter"]

        profile = Profile.objects.get(user=info.context.user)

        if uploaded_audio is None:
            raise GraphQLError("no audiofile recieved")
        else:
            text_from_audio = ""
            
            #try:
            #    raise ValueError('not implemented fully yet')
            #    sound_clasifier = SoundClassifier()
            #    predictions = sound_clasifier.classify_sound(uploaded_audio)

            #    best_keywords = list(map(lambda x: x[0], predictions))

            #    if not set(best_keywords) & set(valid_voice_list):
            #        text_from_audio = "!V! "
            #        #text_from_audio = "Not voice, more likely: " + " or ".join(best_keywords)
            #except Exception as e:
            #    print(e)

            try:
                text_from_audio += transcribe_file(uploaded_audio, profile.language) if (uploaded_audio != None) else None 
            except ValueError as e:
                print(e)

        return Datapoint(
                datetime=datetime,
                category=category,
                image=uploaded_image,
                audio=uploaded_audio,
                source_device=source_device,
                value=value,
                text_from_audio=text_from_audio,
                owner=info.context.user,
            )

    def test(self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):
        return Datapoint(
                datetime=datetime,
                category=category,
                image=None,
                audio=None,
                source_device=source_device,
                value=value,
                text_from_audio=text_from_audio,
                owner=info.context.user)
    
    def weight(self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):
        return Datapoint(
                datetime=datetime,
                category=category,
                image=None,
                audio=None,
                source_device=source_device,
                value=value,
                text_from_audio=text_from_audio,
                owner=info.context.user)

    def shit_cam (self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):
        return Datapoint(
                datetime=datetime,
                category=category,
                image=None,
                audio=None,
                source_device=source_device,
                value=value,
                text_from_audio=text_from_audio,
                owner=info.context.user)
    def food_picture(self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):
        return Datapoint(
                datetime=datetime,
                category=category,
                image=None,
                audio=None,
                source_device=source_device,
                value=value,
                text_from_audio=text_from_audio,
                owner=info.context.user)

    def heart_rate(self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):
        return Datapoint(
                datetime=datetime,
                category=category,
                image=None,
                audio=None,
                source_device=source_device,
                value=value,
                text_from_audio=text_from_audio,
                owner=info.context.user)

    def select_mutate_variant(self, category):
        functionlist = dict()
        for e in CategoryTypes:
            functionlist[e.name] = getattr(CreateDatapoint, e.name)

        # Get the function from functionlist dictionary
        func = functionlist.get(CategoryTypes(category).name)
        # Execute the function
        return func

    @login_required
    def mutate(self, info, category, source_device,
               datetime=None, value=None, text_from_audio=None, files=None):

        function = CreateDatapoint.select_mutate_variant(self, category)

        datapoint = function(self, info, category, source_device,
               datetime, value, text_from_audio, files)
   
        profile = Profile.objects.get(user=info.context.user)
            
        datapoint.save()

        return CreateDatapoint(datapoint=datapoint)
        #    id=datapoint.id,
        #    datetime=datapoint.datetime,
        #    category=datapoint.category,
        #    source_device=datapoint.source_device,
        #    value=datapoint.value,
        #    text_from_audio=datapoint.text_from_audio,
        #    owner=datapoint.owner,
        #)

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
        uploaded_file = info.context.FILES["0"]
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
