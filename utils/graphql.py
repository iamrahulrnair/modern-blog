import graphene
from graphene_django.utils import camelize


class ErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        raise Exception("`errors` should be dict!")


class Mutation(graphene.Mutation):
    class Meta:
        abstract = True

    errors = graphene.Field(ErrorType)
