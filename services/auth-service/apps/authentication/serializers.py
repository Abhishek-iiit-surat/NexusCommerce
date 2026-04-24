from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    provider = serializers.CharField(max_length=50, required=False, allow_blank=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    provider = serializers.CharField(max_length=50, required=False)

    def validate(self, attrs):
        if not attrs.get('username') or not attrs.get('password'):
            raise serializers.ValidationError("Username and password are required.")
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("At least one field must be provided.")
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        return value
