from PersonalDataApi.datapoints.models import Datapoint
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from PersonalDataApi.users.schema import UserType
from django.contrib.auth import get_user_model



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
    name = graphene.String()
    notes = graphene.String()
    owner = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        notes = graphene.String()

    @login_required
    def mutate(self, info, name, notes):

        datapoint = Datapoint(
            name=name,
            notes=notes,
            owner=info.context.user,
        )
        datapoint.save()

        return CreateDatapoint(
            id=datapoint.id,
            name=datapoint.name,
            notes=datapoint.notes,
            owner=datapoint.owner,
        )

class DeleteDatapoint(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    notes = graphene.String()
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
            name=datapoint.name,
            notes=datapoint.notes,
            owner=datapoint.owner
        )

class EditDatapoint(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    notes = graphene.String()
    owner = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        notes = graphene.String()

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
