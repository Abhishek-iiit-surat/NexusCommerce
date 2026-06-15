from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .authentication import JWTUserAuthentication
from .serializers import AddCartItemSerializer, UpdateCartItemSerializer, CartItemResponseSerializer, CartResponseSerializer
from .services import CartService

class InternalCartView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get raw cart items for a user (internal, used by order-service)",
        tags=["Internal"],
        responses={
            200: OpenApiResponse(description="Cart items, no enrichment"),
        },
    )
    def get(self, request, user_id):
        service = CartService()
        items = service.get_cart(user_id)
        data = {
            "user_id": user_id,
            "items": [
                {"product_id": item["product_id"], "quantity": item["quantity"]}
                for item in items
            ],
        }
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Clear a user's cart after order confirmed (internal, used by order-service)",
        tags=["Internal"],
        responses={
            204: OpenApiResponse(description="Cart cleared"),
        },
    )
    def delete(self, request, user_id):
        service = CartService()
        service.clear_cart(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get the current user's cart",
        tags=["Cart"],
        responses={
            200: CartResponseSerializer,
        },
    )
    def get(self, request):
        service = CartService()
        items = service.get_cart(request.user.id)
        data = {"user_id": request.user.id, "items": items}
        return Response(CartResponseSerializer(data).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Clear all items from the current user's cart",
        tags=["Internal"],
        responses={
            200: CartResponseSerializer,
        },
    )
    def delete(self, request):
        service = CartService()
        service.clear_cart(request.user.id)
        data = {"user_id": request.user.id, "items": []}
        return Response(CartResponseSerializer(data).data, status=status.HTTP_200_OK)

class CartItemCreateView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Add an item to the cart",
        tags=["Cart"],
        request=AddCartItemSerializer,
        responses={
            201: OpenApiResponse(description="Item added"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CartService()
        service.add_item(
            user_id=request.user.id,
            product_id=serializer.validated_data['product_id'],
            quantity=serializer.validated_data['quantity'],
        )
        return Response(status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update quantity of a cart item",
        tags=["Cart"],
        request=UpdateCartItemSerializer,
        responses={
            200: OpenApiResponse(description="Quantity updated"),
            400: OpenApiResponse(description="Invalid quantity"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def patch(self, request, product_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CartService()
        service.update_item_quantity(request.user.id, product_id, serializer.validated_data['quantity'])
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="Remove an item from the cart",
        tags=["Cart"],
        responses={
            204: OpenApiResponse(description="Item removed"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def delete(self, request, product_id):
        service = CartService()
        service.remove_item(request.user.id, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
