from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer, OpenApiParameter
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
    
class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new product",
        tags=["Products"],
        request=ProductSerializer,
        responses={
            201: OpenApiResponse(description="Product created successfully"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = ProductService()
        product = service.create_product(created_by_id=request.user.id, **serializer.validated_data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
    
class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update an existing product",
        tags=["Products"],
        request=ProductSerializer,
        responses={
            200: OpenApiResponse(description="Product updated successfully"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Product not found"),
        },
    )
    def put(self, request, id):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = ProductService()
        product = service.update_product(id, **serializer.validated_data)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        
class GetProductDetailsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get details of a specific product",
        tags=["Products"],
        responses={
            200: OpenApiResponse(description="Product details"),
            404: OpenApiResponse(description="Product not found"),
        },
    )
    def get(self, request, id):
        service = ProductService()
        product = service.get_product(id)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    
class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Delete a product",
        tags=["Products"],
        responses={
            204: OpenApiResponse(description="Product deleted successfully"),
            404: OpenApiResponse(description="Product not found"),
        },
    )
    def delete(self, request, id):
        service = ProductService()
        service.delete_product(id)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddProductImageView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Add an image to a product",
        tags=["Products"],
        request=inline_serializer(
            name="AddProductImageRequest",
            fields={
                "image_url": drf_serializers.URLField(),
            }
        ),
        responses={
            200: OpenApiResponse(description="Image added successfully"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Product not found"),
        },
    )
    def post(self, request, product_id):
        serializer = self.get_request_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        image_url = serializer.validated_data['image_url']
        service = ProductService()
        product_image = service.add_product_image(product_id, image_url)
        return Response({
            "id": product_image.id,
            "image_url": product_image.image_url,
            "created_at": product_image.created_at,
            "updated_at": product_image.updated_at,
        }, status=status.HTTP_200_OK)
    
class DeleteProductImageView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Delete an image from a product",
        tags=["Products"],
        responses={
            204: OpenApiResponse(description="Image deleted successfully"),
            404: OpenApiResponse(description="Product or image not found"),
        },
    )
    def delete(self, request, product_id, image_id):
        service = ProductService()
        service.delete_product_image(product_id, image_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



        