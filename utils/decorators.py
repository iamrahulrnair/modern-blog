from graphql_jwt.shortcuts import get_token, get_user_by_token
from graphql_jwt.decorators import context


def authorize(func):
    @context(func)
    def wrapper(context, *args, **kwargs):
        auth_header_info = context.META.get('HTTP_AUTHORIZATION').split(" ")
        if auth_header_info[0] != "JWT": raise Exception("invalid token prefix")
        if auth_header_info[1] == "": raise Exception("invalid token")
        token = auth_header_info[1]
        user = get_user_by_token(token, context)
        return func(user=user, *args, **kwargs)

    return wrapper
