from django.contrib.auth import get_user_model

from graphene import AbstractType, Node, Mutation, String, ObjectType, Field, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        #interfaces = (Node, )
        #filter_fields = {
        #    'username': ['exact', 'icontains', 'istartswith'],
        #    'email': ['exact', 'icontains'],
         #   }

class CreateUser(Mutation):
    user = Field(UserType)

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()


class Query(ObjectType):
    #user = Node.Field(UserType)
    #all_users = DjangoFilterConnectionField(UserType)

    me = Field(UserType)
    all_users = List(UserType)

    
    def resolve_all_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')

        return user
