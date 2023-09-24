import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Post, PostLikes, PostComment


class CommentType(DjangoObjectType):
    class Meta:
        model = PostComment


class PostType(DjangoObjectType):
    class Meta:
        model = Post

    comments = DjangoListField(CommentType)

    def resolve_comments(root, info):
        return PostComment.objects.filter(post=root)


class PostQuery(graphene.ObjectType):
    posts = DjangoListField(PostType)
    post_by_slug = graphene.Field(PostType, slug=graphene.String())

    def resolve_posts(root, info, **kwargs):
        return Post.objects.all()

    def resolve_post_by_slug(root, info, slug):
        return Post.objects.get(slug=slug)


class PostCreate(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, title, content):
        user = "sample"
        post = Post.objects.create_post(title, content, user=user)
        return cls(post=post)


class PostUpdate(graphene.Mutation):
    class Arguments:
        slug = graphene.String()
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, slug, title, content):
        user = "sample"
        post = Post.objects.update_post(title, content, slug, user=user)
        return cls(post=post)


class PostDelete(graphene.Mutation):
    class Arguments:
        slug = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, slug):
        user = "sample"
        post = Post.objects.delete_post(slug, user)
        return cls(post=post)


class PostMutations(graphene.ObjectType):
    create_post = PostCreate.Field()
    update_post = PostUpdate.Field()
    delete_post = PostDelete.Field()
