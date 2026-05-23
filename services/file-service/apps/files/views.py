from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .authentication import JWTUserAuthentication
from .serializers import FileResponseSerializer, FileUploadSerializer
from .services import FileService
from .permissions import IsAdminOrSeller

class FileUploadView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    @extend_schema(
        summary="Upload a file",
        tags=["Files"],
        request={
          'multipart/form-data': FileUploadSerializer
        },
        responses={
            201: OpenApiResponse(response=FileResponseSerializer, description="File uploaded successfully"),
            400: OpenApiResponse(description="Validation error"),
            500: OpenApiResponse(description="File upload error"),
        },
    )
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        file = serializer.validated_data['file']
        service = FileService()
        new_file = service.upload_file(request.user.id, **serializer.validated_data)
        return Response(FileResponseSerializer(new_file).data, status=status.HTTP_201_CREATED)
    
class FileDetailView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    @extend_schema(
        summary="Get file details",
        tags=["Files"],
        parameters=[
            OpenApiParameter(name="file_id", description="ID of the file to retrieve", required=True, type=int)
        ],
        responses={
            200: OpenApiResponse(response=FileResponseSerializer, description="File details retrieved successfully"),
            404: OpenApiResponse(description="File not found"),
        },
    )
    def get(self, request, file_id):
        service = FileService()
        file = service.get_file(file_id)
        return Response(FileResponseSerializer(file).data, status=status.HTTP_200_OK)
    
class FileDeleteView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    @extend_schema(
        summary="Delete a file",
        tags=["Files"],
        parameters=[
            OpenApiParameter(name="file_id", description="ID of the file to delete", required=True, type=int)
        ],
        responses={
            204: OpenApiResponse(description="File deleted successfully"),
            404: OpenApiResponse(description="File not found"),
        },
    )
    def delete(self, request, file_id):
        service = FileService()
        service.delete_file(file_id, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)