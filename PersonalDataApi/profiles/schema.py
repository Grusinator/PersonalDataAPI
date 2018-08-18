
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphene_file_upload import Upload

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from PersonalDataApi.users.schema import UserType
from django.contrib.auth import get_user_model

from PersonalDataApi.datapoints.models import Datapoint, CategoryTypes
from PersonalDataApi.profiles.models import Profile, Languages


GrapheneLanguages = graphene.Enum.from_enum(Languages)

#class ProfileType(DjangoObjectType):
#    class Meta:
#        model = Profile
#        # Allow for some more advanced filtering here
#        #interfaces = (graphene.Node, )
#        #filter_fields = {
#        #    'name': ['exact', 'icontains', 'istartswith'],
#        #    'notes': ['exact', 'icontains'],
#        #}

#class UpdateProfile(graphene.Mutation):
#    user = graphene.Field(UserType)
#    name = graphene.String()
#    birthdate = graphene.Date()
#    language = GrapheneLanguages()
#    profilepicture = Upload()
#    audio_threshold = graphene.Float()

#    class Arguments:
#        name = graphene.String()
#        birthdate = graphene.Date()
#        language = GrapheneLanguages()
#        #profilepicture = Upload()
#        audio_threshold = graphene.Float()


#    @login_required
#    def mutate(self, info, language, audio_threshold, name=None, birthdate=None):
#        try:
#            profile = Profile.objects.get(owner=info.context.user) 
#        except:
#            raise GraphQLError("profile object has not been created successfully")

#        #update each attribute
#        if name is not None:
#            profile.name=name
#        if birthdate is not None:
#            profile.birthdate=birthdate
#        if language is not None:
#            profile.language=language
#        if audio_threshold is not None:
#            profile.audio_threshold=audio_threshold

#        profile.save()

#        return UpdateProfile(
#            name=profile.name,
#            birthdate=profile.birthdate,
#            language=profile.language,
#            audio_threshold=profile.audio_threshold,
#            user=profile.user
#        )


#class Query(graphene.ObjectType):
#    profile = graphene.Field(ProfileType)

#    @login_required
#    def resolve_profile(self, info):

#        profile = Profile.objects.filter(owner=info.context.user).first()
#        return profile


#class Mutation(graphene.ObjectType):
#    update_profile = UpdateProfile.Field()

