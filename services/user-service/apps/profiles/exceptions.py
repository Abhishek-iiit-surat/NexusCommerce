from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class ProfileNotFoundError(Exception):
    pass


class AddressNotFoundError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass

class CannotUpdateUserProfileError(Exception):
    pass

class UserProfileAlreadyExistsError(Exception):
    pass

def custom_exception_handler(exc, context):
    if isinstance(exc, ProfileNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, AddressNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, PermissionDeniedError):
        return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
    
    if isinstance(exc, CannotUpdateUserProfileError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exc, UserProfileAlreadyExistsError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return exception_handler(exc, context)
