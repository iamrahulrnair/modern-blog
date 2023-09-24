import graphene
from posts.schema import PostQuery


class Query(PostQuery, graphene.ObjectType):
    pass


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)
