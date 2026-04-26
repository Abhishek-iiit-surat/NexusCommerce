from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .services import ProfileService, AddressService
from .serializers import UserProfileSerializer, AddressSerializer


# TODO: implement ProfileView (GET, PUT) — /me/
# TODO: implement AddressListCreateView (GET, POST) — /addresses/
# TODO: implement AddressDetailView (PUT, DELETE) — /addresses/{id}/
# TODO: implement AddressSetDefaultView (PATCH) — /addresses/{id}/set-default/
# TODO: implement InternalProfileView (GET) — /internal/{user_id}/
# TODO: implement HealthCheckView (GET) — /health/
