from .exceptions import (
    ProfileNotFoundError, 
    AddressNotFoundError, 
    PermissionDeniedError,
    CannotUpdateUserProfileError,
    UserProfileAlreadyExistsError
    )
from .models import (
    UserProfile, 
    Address
)



class ProfileService:
    def get_profile(self,user_id):
        user_obj = UserProfile.objects.filter(user_id=user_id).first()
        if user_obj is None:
            raise ProfileNotFoundError(f"Profile for user_id {user_id} not found.")
        return user_obj

    def create_profile(self, user_id, **profile_details):
        if UserProfile.objects.filter(user_id=user_id).first() is not None:
            raise UserProfileAlreadyExistsError(f"Profile for user_id {user_id} already exists.")
        profile = UserProfile(user_id=user_id, **profile_details)
        profile.save()
        return profile_details
    
    def update_userprofile(self, user_id, **profile_details):
        if UserProfile.objects.filter(user_id=user_id).first() is None:
            raise ProfileNotFoundError(f"Profile for user_id {user_id} not found.")
        profile = UserProfile.objects.filter(user_id=user_id).first()
        for key,value in profile_details.items():
            setattr(profile, key, value)
        profile.save()
        return profile_details



class AddressService:
    # TODO: implement list_addresses(user_id)
    # TODO: implement add_address(user_id, **kwargs)
    # TODO: implement update_address(user_id, address_id, **kwargs)
    # TODO: implement delete_address(user_id, address_id)
    # TODO: implement set_default_address(user_id, address_id, address_type)
    pass
