
from .models import User, AuthToken
class EmailOrMobileBackend:
    def authenticate(self, request, **credentials):
        username = credentials.get('username')
        password = credentials.get('password')
        if not username or not password:
            return None
        
        is_email = '@' in username
        user = None
        if is_email:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(mobile_number=username).first()

        if not user:
            return None
        
        if user and user.check_password(password):
            return user
        if user and not user.check_password(password):
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None