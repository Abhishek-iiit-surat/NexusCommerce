from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class ProductNotFoundError(Exception):
    pass


class CategoryNotFoundError(Exception):
    pass


class ProductAlreadyExistsError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


def custom_exception_handler(exc, context):
    if isinstance(exc, ProductNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, CategoryNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, ProductAlreadyExistsError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, PermissionDeniedError):
        return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    return exception_handler(exc, context)
