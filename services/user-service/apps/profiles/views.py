from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .services import (
    ProfileService,
    AddressService
    )
from .serializers import (
    UserProfileSerializer,
    AddressSerializer
    )


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Health check",
        description="Returns 200 if the user-service is up.",
        responses={200: OpenApiResponse(description="Service is healthy")},
        tags=["Health"],
    )
    def get(self, request):
        return Response({"detail": "User Service is up and running"}, status=status.HTTP_200_OK)


class InternalProfileView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Internal — get profile by user_id",
        description="Used by other services to fetch a user profile by user_id. No authentication required. Not intended for public clients.",
        parameters=[OpenApiParameter("user_id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={
            200: UserProfileSerializer,
            404: OpenApiResponse(description="Profile not found"),
        },
        tags=["Internal"],
    )
    def get(self, request, user_id):
        service = ProfileService()
        profile = service.get_user_profile(user_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get my profile",
        description="Returns the profile of the currently authenticated user.",
        responses={
            200: UserProfileSerializer,
            404: OpenApiResponse(description="Profile not found"),
        },
        tags=["Profile"],
    )
    def get(self, request):
        user_id = request.user.id
        service = ProfileService()
        profile = service.get_user_profile(user_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create my profile",
        description="Creates a profile for the currently authenticated user. Fails if one already exists.",
        request=UserProfileSerializer,
        responses={
            201: UserProfileSerializer,
            400: OpenApiResponse(description="Validation error or profile already exists"),
        },
        tags=["Profile"],
    )
    def post(self, request):
        user_id = request.user.id
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = ProfileService()
        user_profile = service.create_user_profile(user_id, **serializer.validated_data)
        user_profile_serialized = UserProfileSerializer(user_profile)
        return Response(user_profile_serialized.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update my profile",
        description="Updates the profile of the currently authenticated user.",
        request=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Profile not found"),
        },
        tags=["Profile"],
    )
    def put(self, request):
        user_id = request.user.id
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = ProfileService()
        updated_profile = service.update_user_profile(user_id, **serializer.validated_data)
        updated_profile_serialized = UserProfileSerializer(updated_profile)
        return Response(updated_profile_serialized.data, status=status.HTTP_200_OK)


class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List my addresses",
        description="Returns all addresses belonging to the currently authenticated user.",
        responses={200: AddressSerializer(many=True)},
        tags=["Addresses"],
    )
    def get(self, request):
        user_id = request.user.id
        service = AddressService()
        addresses = service.list_address(user_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Add an address",
        description="Creates a new address for the currently authenticated user.",
        request=AddressSerializer,
        responses={
            201: AddressSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
        tags=["Addresses"],
    )
    def post(self, request):
        user_id = request.user.id
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = AddressService()
        address = service.add_address(user_id, **serializer.validated_data)
        address_serialized = AddressSerializer(address)
        return Response(address_serialized.data, status=status.HTTP_201_CREATED)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update an address",
        description="Updates an existing address by ID for the currently authenticated user.",
        parameters=[OpenApiParameter("address_id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        request=AddressSerializer,
        responses={
            200: AddressSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Address not found"),
        },
        tags=["Addresses"],
    )
    def put(self, request, address_id):
        user_id = request.user.id
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = AddressService()
        updated_address = service.update_address(user_id, address_id, **serializer.validated_data)
        updated_address_serialized = AddressSerializer(updated_address)
        return Response(updated_address_serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete an address",
        description="Deletes an address by ID for the currently authenticated user.",
        parameters=[OpenApiParameter("address_id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={
            204: OpenApiResponse(description="Address deleted"),
            404: OpenApiResponse(description="Address not found"),
        },
        tags=["Addresses"],
    )
    def delete(self, request, address_id):
        user_id = request.user.id
        service = AddressService()
        service.delete_address(user_id, address_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressSetDefaultView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Set default address",
        description="Sets an address as the default shipping or billing address. Send `default_type` as `shipping` or `billing` in the request body.",
        parameters=[OpenApiParameter("address_id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={
            200: AddressSerializer,
            400: OpenApiResponse(description="Invalid or missing default_type"),
            404: OpenApiResponse(description="Address not found"),
        },
        tags=["Addresses"],
    )
    def patch(self, request, address_id):
        default_type = request.data.get("default_type")
        user_id = request.user.id

        service = AddressService()
        if default_type.lower() == "shipping":
            updated_address = service.set_default_shipping(user_id, address_id)
        elif default_type.lower() == "billing":
            updated_address = service.set_default_billing(user_id, address_id)
        else:
            return Response({"detail": "Invalid default_type. Must be 'shipping' or 'billing'."}, status=status.HTTP_400_BAD_REQUEST)

        updated_address_serialized = AddressSerializer(updated_address)
        return Response(updated_address_serialized.data, status=status.HTTP_200_OK)
