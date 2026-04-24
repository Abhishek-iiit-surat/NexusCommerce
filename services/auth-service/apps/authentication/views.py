from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers as drf_serializers

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UpdateUserSerializer,
    ResetPasswordSerializer,
)
from .services import AuthService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Register a new user",
        tags=["Auth"],
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Registered successfully, returns access and refresh tokens"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = AuthService()
        tokens = service.register_user(**serializer.validated_data)
        return Response(tokens, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Login with email or mobile number",
        tags=["Auth"],
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful, returns access and refresh tokens"),
            400: OpenApiResponse(description="Validation error or invalid credentials"),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = AuthService()
        tokens = service.login_user(request, **serializer.validated_data)
        if tokens is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(tokens, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout and blacklist refresh token",
        tags=["Auth"],
        request=LogoutSerializer,
        responses={
            200: OpenApiResponse(description="Logged out successfully"),
            400: OpenApiResponse(description="Invalid or missing refresh token"),
        },
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = AuthService()
        try:
            service.logout_user(serializer.validated_data['refresh_token'])
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Refresh access token",
        tags=["Auth"],
        request=inline_serializer(
            name="RefreshTokenRequest",
            fields={"refresh_token": drf_serializers.CharField()},
        ),
        responses={
            200: OpenApiResponse(description="Returns new access and refresh tokens"),
            400: OpenApiResponse(description="Invalid or missing refresh token"),
        },
    )
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        service = AuthService()
        try:
            tokens = service.refresh_token(refresh_token)
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update user details",
        tags=["Auth"],
        request=UpdateUserSerializer,
        responses={
            200: OpenApiResponse(description="User details updated successfully"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def put(self, request):
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = AuthService()
        try:
            updated_fields = service.update_user_details(request.user.id, **serializer.validated_data)
            return Response({"detail": "User details updated successfully", "updated_fields": updated_fields}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Reset user password",
        tags=["Auth"],
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password reset successfully, returns new tokens"),
            400: OpenApiResponse(description="Validation error or incorrect old password"),
        },
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = AuthService()
        try:
            tokens = service.reset_password(request.user.id, serializer.validated_data['new_password'])
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Delete (soft-delete) the authenticated user",
        tags=["Auth"],
        responses={
            200: OpenApiResponse(description="User deleted successfully"),
            400: OpenApiResponse(description="Error deleting user"),
        },
    )
    def delete(self, request):
        service = AuthService()
        try:
            result = service.delete_user(request.user.id)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get authenticated user details",
        tags=["Auth"],
        responses={
            200: OpenApiResponse(description="Returns user profile details"),
        },
    )
    def get(self, request):
        user = request.user
        user_data = {
            "email": user.email,
            "mobile_number": user.mobile_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "provider": user.login_provider,
        }
        return Response(user_data, status=status.HTTP_200_OK)

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Health check",
        tags=["Health"],
        responses={
            200: OpenApiResponse(description="Service is up and running"),
        },
    )
    def get(self, request):
        return Response(
            {
                "status": "ok",
                "message": "Authentication service is up and running"
            }
            , status=status.HTTP_200_OK
        )
