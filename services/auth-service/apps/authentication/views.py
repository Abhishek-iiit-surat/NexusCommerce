from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import (
    RegisterSerializer, 
    LoginSerializer,
    UpdateUserSerializer,
    ResetPasswordSerializer
    
    )
from .services import AuthService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: call AuthService and return tokens
        # service = AuthService()
        # tokens = service.register_user(**serializer.validated_data)
        # return Response(tokens, status=status.HTTP_201_CREATED)
        service = AuthService()
        tokens = service.register_user(**serializer.validated_data)
        return Response(tokens, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: call AuthService and return tokens
        # service = AuthService()
        # tokens = service.login_user(**serializer.validated_data)
        # return Response(tokens, status=status.HTTP_200_OK)

        service = AuthService()
        tokens = service.login_user(**serializer.validated_data)
        return Response(tokens, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = AuthService()
        try:
            service.logout_user(serializer.validated_data['refresh_token'])
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RefreshTokenView(APIView):
    permission_classes = [permissions.allowAny]
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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        service = AuthService()
        try:
            tokens = service.reset_password(request.user.id, **serializer.validated_data)
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        service = AuthService()
        try:
            result = service.delete_user(request.user.id)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetUserDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "email": user.email,
            "mobile_number": user.mobile_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "provider": user.provider,
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
class HealthCheckView(APIView):
    permission_classes = [permissions.allowAny]

    def get(self):
        return Response(
            {
                "status": "ok",
                "message": "Authentication service is up and running"
            }
            , status=status.HTTP_200_OK
        )
