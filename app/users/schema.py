import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # if you want to restrict to only these fields
        # fields = ('id', 'email', 'password', 'username')


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.UUID(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if(user.is_anonymous):
            raise Exception('Not logged in!')
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username: str, password: str, email: str):
        user = User(username=username, email=email)
        user.set_password(password)

        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
