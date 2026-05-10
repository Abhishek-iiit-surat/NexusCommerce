from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .authentication import JWTUserAuthentication
from .serializers import CartSerializer, CartItemSerializer
from .services import CartService, CartItemService


class CartView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get the current user's cart",
        tags=["Cart"],
        responses={
            200: CartSerializer,
            404: OpenApiResponse(description="Cart not found"),
        },
    )
    def get(self, request):
        service = CartService()
        cart = service.get_or_create_cart(request.user.id)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Clear all items from the current user's cart",
        tags=["Cart"],
        responses={
            200: CartSerializer,
            404: OpenApiResponse(description="Cart not found"),
        },
    )
    def delete(self, request):
        service = CartService()
        cart = service.clear_cart(request.user.id)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartItemCreateView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Add an item to the cart",
        tags=["Cart"],
        request=CartItemSerializer,
        responses={
            201: CartItemSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = CartItemService()
        item = service.add_item(
            user_id=request.user.id,
            product_id=serializer.validated_data['product_id'],
            product_name=serializer.validated_data['product_name'],
            price_snapshot=serializer.validated_data['price_snapshot'],
            quantity=serializer.validated_data.get('quantity', 1),
        )
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update quantity of a cart item",
        tags=["Cart"],
        request=CartItemSerializer,
        responses={
            200: CartItemSerializer,
            400: OpenApiResponse(description="Invalid quantity"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def patch(self, request, item_id):
        quantity = request.data.get('quantity')
        if quantity is None:
            return Response({"detail": "quantity is required."}, status=status.HTTP_400_BAD_REQUEST)
        service = CartItemService()
        item = service.update_item_quantity(request.user.id, item_id, int(quantity))
        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Remove an item from the cart",
        tags=["Cart"],
        responses={
            204: OpenApiResponse(description="Item removed"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def delete(self, request, item_id):
        service = CartItemService()
        service.remove_item(request.user.id, item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
