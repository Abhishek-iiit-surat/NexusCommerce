from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidTokenError(Exception):
    pass

class TokenError(Exception):
    pass


def custom_exception_handler(exc, context):
    if isinstance(exc, UserAlreadyExistsError):
        return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

    if isinstance(exc, InvalidCredentialsError):
        return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, UserNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, InvalidTokenError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return exception_handler(exc, context)
