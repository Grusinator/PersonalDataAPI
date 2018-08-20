import PersonalDataApi.datapoints.schema
import PersonalDataApi.users.schema
import graphene
import graphql_jwt



from graphene_django.debug import DjangoDebug


class Query(
    PersonalDataApi.users.schema.Query, 
    PersonalDataApi.datapoints.schema.Query, 
    graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

class Mutation(
    PersonalDataApi.users.schema.Mutation, 
    PersonalDataApi.datapoints.schema.Mutation, 

    graphene.ObjectType):
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query, mutation=Mutation)
