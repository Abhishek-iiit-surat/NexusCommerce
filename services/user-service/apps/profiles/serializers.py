from rest_framework import serializers
from .models import UserProfile, Address


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id', 'avatar', 'dob', 'bio', 'gender', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user_id', 'label', 'full_name', 'phone_number', 'address_line1', 'address_line2',
                  'city', 'state', 'country', 'pincode','created_at', 'updated_at']
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at']