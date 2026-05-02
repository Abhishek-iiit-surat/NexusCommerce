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
    def get_user_profile(self,user_id):
        user_obj = UserProfile.objects.filter(user_id=user_id).first()
        if user_obj is None:
            raise ProfileNotFoundError(f"Profile for user_id {user_id} not found.")
        return user_obj

    def create_user_profile(self, user_id, **profile_details):
        if UserProfile.objects.filter(user_id=user_id).first() is not None:
            raise UserProfileAlreadyExistsError(f"Profile for user_id {user_id} already exists.")
        profile = UserProfile(user_id=user_id, **profile_details)
        profile.save()
        return profile
    
    def update_user_profile(self, user_id, **profile_details):
        if UserProfile.objects.filter(user_id=user_id).first() is None:
            raise ProfileNotFoundError(f"Profile for user_id {user_id} not found.")
        profile = UserProfile.objects.filter(user_id=user_id).first()
        for key,value in profile_details.items():
            setattr(profile, key, value)
        profile.save()
        return profile



class AddressService:

    def list_address(self, user_id):
        addresses = Address.objects.filter(user_id=user_id)
        return addresses
    
    def add_address(self, user_id, **address_details):
        address = Address(user_id=user_id, **address_details)
        address.save()
        return address
    
    def update_address(self, user_id, address_id, **address_details):
        address = Address.objects.filter(user_id=user_id, id=address_id).first()
        if address is None:
            raise AddressNotFoundError(f"Address with id {address_id} not found for user_id {user_id}.")
        for key, value in address_details.items():
            setattr(address,key,value)
        address.save()
        return address
    
    def delete_address(self, user_id, address_id):
        address = Address.objects.filter(user_id=user_id, id=address_id).first()
        if address is None:
            raise AddressNotFoundError(f"Address with id {address_id} not found for user_id {user_id}.")
        address.delete()
        return True
    
    def set_default_billing(self, user_id, address_id):
        address = Address.objects.filter(user_id=user_id, id=address_id).first()
        Address.objects.filter(user_id=user_id).update(is_default_billing=False)
        if address is None:
            raise AddressNotFoundError(f"Address with id {address_id} not found for user_id {user_id}.")
        address.is_default_billing = True
        address.save()
        return address

    def set_default_shipping(self, user_id, address_id):
        address = Address.objects.filter(user_id=user_id, id=address_id).first()
        Address.objects.filter(user_id = user_id).update(is_default_shipping=False)
        if address is None:
            raise AddressNotFoundError(f"Address with id {address_id} not found for user_id {user_id}.")
        address.is_default_shipping = True
        address.save()
        return address

        
