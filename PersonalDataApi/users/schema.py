from django.contrib.auth import get_user_model

from graphene import AbstractType, Node, Mutation, String, ObjectType, Field, List, Date, Enum, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from PersonalDataApi.users.models import Profile, Languages
from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

GrapheneLanguages = Enum.from_enum(Languages)

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        #interfaces = (Node, )
        #filter_fields = {
        #    'username': ['exact', 'icontains', 'istartswith'],
        #    'email': ['exact', 'icontains'],
         #   }

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        # Allow for some more advanced filtering here
        #interfaces = (graphene.Node, )
        #filter_fields = {
        #    'name': ['exact', 'icontains', 'istartswith'],
        #    'notes': ['exact', 'icontains'],
        #}

class CreateUser(Mutation):
    user = Field(UserType)


    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)
        birthdate = Date()
        language = GrapheneLanguages()

    def mutate(self, info, username, password, email, birthdate=None, language="English"):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile = Profile(
            birthdate=birthdate,
            user=user,
            language=language
        )
        profile.save()

        return CreateUser(user=user)


class UpdateProfile(Mutation):
    profile = Field(ProfileType)

    class Arguments:
        birthdate = Date()
        language = GrapheneLanguages()
        #profilepicture = Upload()
        audio_threshold = Float()


    @login_required
    def mutate(self, info, language, audio_threshold, birthdate=None):
        try:
            profile = Profile.objects.get(user=info.context.user)
        except Exception as e:
            raise GraphQLError("profile object has not been created successfully: " + str(e))

        #update each attribute
        if birthdate is not None:
            profile.birthdate=birthdate
        if language is not None:
            profile.language=language
        if audio_threshold is not None:
            profile.audio_threshold=audio_threshold

        profile.save()

        return UpdateProfile(profile)

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()


class Query(ObjectType):
    user = Field(UserType)
    profile = Field(ProfileType)

    @login_required
    def resolve_user(self, info):
        return info.context.user

    @login_required
    def resolve_profile(self, info):
        return Profile.objects.get(user=info.context.user)
         
