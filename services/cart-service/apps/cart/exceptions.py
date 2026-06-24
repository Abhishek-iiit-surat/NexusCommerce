from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class CartNotFoundError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass


class ProductUnavailableError(Exception):
    pass

class UnexpectedError(Exception):
    pass


def custom_exception_handler(exc, context):
    if isinstance(exc, CartNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, CartItemNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, InvalidQuantityError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, ProductUnavailableError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    
    if isinstance(exc, UnexpectedError):
        return Response({"detail": str(exc)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return exception_handler(exc, context)
