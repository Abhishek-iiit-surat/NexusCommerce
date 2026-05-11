from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class OrderNotFoundError(Exception):
    pass


class OrderItemNotFoundError(Exception):
    pass


class InvalidOrderStatusError(Exception):
    pass


class OrderCancellationError(Exception):
    pass


def custom_exception_handler(exc, context):
    if isinstance(exc, OrderNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, OrderItemNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, InvalidOrderStatusError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, OrderCancellationError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return exception_handler(exc, context)
