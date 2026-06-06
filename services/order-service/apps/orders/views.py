from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .authentication import JWTUserAuthentication
from .serializers import CreateOrderSerializer, OrderSerializer, UpdateOrderStatusSerializer
from .services import PlaceOrderService


class PlaceOrderView(APIView):
    authentication_classes = [JWTUserAuthentication]

    @extend_schema(
        summary="Place a new order",
        request=CreateOrderSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Validation error or empty items"),
        },
        tags=["Orders"],
    )
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.valid():
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        service = PlaceOrderService()
        order = service.create_order(user_id = request.user_id, *serializer.validated_data)


class MyOrdersView(APIView):
    authentication_classes = [JWTUserAuthentication]

    @extend_schema(
        summary="List all orders for the authenticated user",
        responses={
            200: OrderSerializer(many=True),
        },
        tags=["Orders"],
    )
    def get(self, request):
        pass


class OrderDetailView(APIView):
    authentication_classes = [JWTUserAuthentication]

    @extend_schema(
        summary="Get a single order by ID (owner only)",
        responses={
            200: OrderSerializer,
            404: OpenApiResponse(description="Order not found"),
        },
        tags=["Orders"],
    )
    def get(self, request, order_id):
        pass


class CancelOrderView(APIView):
    authentication_classes = [JWTUserAuthentication]

    @extend_schema(
        summary="Cancel an order (owner only, pending/confirmed only)",
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Order cannot be cancelled in its current status"),
            404: OpenApiResponse(description="Order not found"),
        },
        tags=["Orders"],
    )
    def patch(self, request, order_id):
        pass


class AdminUpdateStatusView(APIView):
    authentication_classes = [JWTUserAuthentication]

    @extend_schema(
        summary="Update order status (admin only)",
        request=UpdateOrderStatusSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Invalid status value"),
            403: OpenApiResponse(description="Admin role required"),
            404: OpenApiResponse(description="Order not found"),
        },
        tags=["Orders - Admin"],
    )
    def patch(self, request, order_id):
        pass
