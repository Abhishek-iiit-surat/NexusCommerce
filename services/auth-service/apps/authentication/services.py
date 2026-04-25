# TODO: implement business logic
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, AuthToken
from django.contrib.auth import authenticate
from .exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError, InvalidTokenError


class AuthService():
    # inside this we will define functions related to authentication 

    def __init__(self):
        self.user_model = User
        self.auth_token_model = AuthToken


    def register_user(self, email, password, mobile_number, first_name, last_name = None, provider=None):
        
        if self.user_model.objects.filter(email = email).exists():
            raise UserAlreadyExistsError("Email already exists")
        if self.user_model.objects.filter(mobile_number = mobile_number).exists():
            raise UserAlreadyExistsError("Mobile number already exists")
        user = self.user_model.objects.create_user(
            email =  email,
            first_name = first_name,
            last_name = last_name,
            mobile_number = mobile_number,
            password = password,
            login_provider = provider
        )
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            "access_token": str(access),
            "refresh_token": str(refresh)
        }
     

    def login_user(self, request, username, password, provider=None):

        user  = authenticate(request, username=username,password=password)
        if user is None:
            raise InvalidCredentialsError("Invalid username or password")
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def refresh_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        except TokenError:
            raise InvalidTokenError("Error refreshing token. Please login again.")

    def logout_user(self, refresh_token):

        # get the user from the request and then do is_active false and delete access token
        # and refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        return {"message":"User logged out successfully"}


    def delete_user(self, user_id):
        user = self.user_model.objects.filter(id = user_id).first()
        if not user:
            raise UserNotFoundError("User Does not Exists")
        user.delete()
        return {"message":"User deleted successfully"}
    


    def update_user_details(self, user_id, **kwargs):
        user = self.user_model.objects.filter(id=user_id).first()
        updated_fields = {}
        if not user:
            raise UserNotFoundError("User Does not Exists") 
        
        for key, value in kwargs.items():
            if key.lower() in ['email', 'mobile_number', 'password']:
                continue
            updated_fields[key] = value
            setattr(user, key, value)

        user.save()

        return updated_fields

        
    def reset_password(self,user_id,new_password):
        user = self.user_model.objects.filter(id=user_id).filter(is_active=True).first()
        if not user:
            raise UserNotFoundError("No active user found with this id")
        
        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }


    def get_user_details(self, user_id):
        user = self.user_model.objects.filter(id=user_id, is_active=True).first()
        if not user:
            raise UserNotFoundError("No active user found with this id")
        return {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobile_number": user.mobile_number,
            "is_verified": user.is_verified,
        }
    