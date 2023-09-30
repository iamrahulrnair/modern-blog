import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphql_jwt
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token, get_user_by_token

from utils.decorators import authorize


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class SignupMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        confirm_password = kwargs.get('confirm_password')
        if password != confirm_password:
            raise GraphQLError("Passwords doesnt match")
        user = get_user_model().objects.filter(email=email).first()
        if user:
            raise GraphQLError("email or password doesn't match")
        user = get_user_model()(email=email)
        user.set_password(password)
        user.save()
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        return cls(user=user, token=token, refresh_token=refresh_token)


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    signup = SignupMutation.Field()


class AuthQueries(graphene.ObjectType):
    me = graphene.Field(UserType)

    @authorize
    def resolve_me(root, info, user, *args, **kwargs):
        return user
