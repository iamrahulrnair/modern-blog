import graphene
from posts.schema import PostQuery, PostMutations
from users.schema import AuthQueries, AuthMutation


class Query(PostQuery, AuthQueries, graphene.ObjectType):
    pass


class Mutation(PostMutations, AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
