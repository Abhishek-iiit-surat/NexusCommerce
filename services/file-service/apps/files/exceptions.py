from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class FileNotFoundException(Exception):
    pass


class FileSizeLimitExceededError(Exception):
    pass

class FileUploadError(Exception):
    pass

class UnsupportedFileFormatError(Exception):
    pass

def custom_exception_handler(exc, context):
    if isinstance(exc, FileNotFoundException):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, FileSizeLimitExceededError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, FileUploadError):
        return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc, UnsupportedFileFormatError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return exception_handler(exc, context)
