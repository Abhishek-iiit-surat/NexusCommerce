from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers as drf_serializers
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)
from .services import CategoryService, ProductService



class ListProductCategoriesView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List all active product categories",
        tags=["Products"],
        responses={
            200: OpenApiResponse(description="List of active categories"),
        },
    )
    def get(self, request):
        service = CategoryService()
        categories = service.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateProductCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new product category",
        tags=["Products"],
        request=CategorySerializer,
        responses={
            201: OpenApiResponse(description="Category created successfully"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = CategoryService()
        category = service.create_category(**serializer.validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
    
class UpdateProductCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update an existing product category",
        tags=["Products"],
        request=CategorySerializer,
        responses={
            200: OpenApiResponse(description="Category updated successfully"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Category not found"),
        },
    )
    def put(self, request, id):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = CategoryService()
        category = service.update_category(id, **serializer.validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_200_OK)
    
class ListProductsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List all active products with pagination and optional category filter",
        tags=["Products"],
        parameters=[
            OpenApiParameter(name="page", type=int, description="Page number"),
            OpenApiParameter(name="page_size", type=int, description="Number of items per page"),
            OpenApiParameter(name="category_id", type=int, description="Filter by category ID"),
        ],
        responses={
            200: OpenApiResponse(description="List of active products"),
        },
    )
    def get(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        category_id = request.query_params.get('category_id')
        service = ProductService()
        products, total_pages = service.get_all_products(page=page, page_size=page_size, category_id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response({
            "products": serializer.data,
            "total_pages": total_pages
        }, status=status.HTTP_200_OK)
        

        