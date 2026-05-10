from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class JWTUser:
    """Minimal user object populated from JWT claims. No database hit."""
    def __init__(self, user_id, role):
        self.id = user_id
        self.is_authenticated = True
        self.role = role

        #Note:
        # django internally sets request.user = JWTUSer
        #  now when using in views when we do request.user.id we get the id which we have set in the consructor
        


class JWTUserAuthentication(BaseAuthentication):
    """
    Decodes the Bearer JWT and returns a lightweight JWTUser.
    No Django User model or auth-service call needed.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        raw_token = auth_header.split(' ')[1]
        try:
            token = AccessToken(raw_token)
            user_id = token['user_id']
            role = token.get('role','buyer')
        except TokenError:
            raise AuthenticationFailed("Invalid or expired token.")

        return (JWTUser(user_id,role), token)
