# TODO: implement business logic
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, AuthToken


class AuthService():
    # inside this we will define functions related to authentication 

    def __init__(self):
        self.user_model = User
        self.auth_token_model = AuthToken


    def register_user(self, email, password, mobile_number, first_name, last_name = None, provider=None):
        try:
            if self.user_model.objects.filter(email = email).exists():
                raise ValueError("Email already exists")
            if self.user_model.objects.filter(mobile_number = mobile_number).exists():
                raise ValueError("Mobile number already exists")
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
        except Exception as e:
            raise ValueError(str(e))

    def login_user(self, password, email=None, mobile_number=None, provider=None):
        if email:
            user = self.user_model.objects.filter(email=email).first()
            if not user:
                raise ValueError("User with this email does not exist")
        elif mobile_number:
            user = self.user_model.objects.filter(mobile_number=mobile_number).first()
            if not user:
                raise ValueError("User with this mobile number does not exist")
        else:
            raise ValueError("Email or mobile number is required")

        if not user.check_password(password):
            raise ValueError("Invalid password")
        
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def refresh_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        except TokenError:
            raise ValueError("Invalid refresh token")

    def logout_user(self, user_id):

        # get the user from the request and then do is_active false and delete access token
        # and refresh token
        user = self.user_model.objects.filter(id=user_id).first()
        if not user:
            raise ValueError("User Does not Exists")
        user.is_active = False
        user.access_token = None
        user.refresh_token = None
        user.save()
        return {"message":"User logged out successfully"}


    def delete_user(self, user_id):
        user = self.user_model.objects.filter(id = user_id).first()
        if not user:
            raise ValueError("User Does not Exists")
        user.delete()
        return {"message":"User deleted successfully"}
    


    def update_user_details(self, user_id, **kwargs):
        user = self.user_model.objects.filter(id=user_id).first()
        if not user:
            raise ValueError("User Does not Exists")
        
        for key, value in kwargs.items():
            if key.lower() in ['email','mobile_number']:
                continue
            setattr(user,key,value)

        user.save()

    
    def reset_password(self,user_id,new_password):
        user = self.user_model.objects.filter(id=user_id).filter(is_active=True).first()
        if not user:
            raise ValueError("No active user found with this id")
        
        user.set_password(new_password)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return {
            "access_token": str(access),
            "refresh_token": str(refresh)
        }


    def refresh_token(self,refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        except TokenError:
            raise ValueError("Invalid refresh token")
        

    def get_user_details(self,user_id):
        user = self.user_model.objects.filter(id=user_id).filter(is_active=True).first()
        return{
            "email":user.email,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "mobile_number":user.mobile_number,
            "is_verified":user.is_verified
        }
    