from django.urls import path
from .views import (
    ListProductCategoriesView,
    CreateProductCategoryView,
    UpdateProductCategoryView,
    ListProductsView,
    CreateProductView,
    GetProductDetailsView,
    UpdateProductView,
    DeleteProductView,
    AddProductImageView,
    DeleteProductImageView,
)

urlpatterns = [
    path('categories/', ListProductCategoriesView.as_view()),
    path('categories/create/', CreateProductCategoryView.as_view()),
    path('categories/<int:id>/', UpdateProductCategoryView.as_view()),
    path('', ListProductsView.as_view()),
    path('create/', CreateProductView.as_view()),
    path('<int:id>/', GetProductDetailsView.as_view()),
    path('<int:id>/update/', UpdateProductView.as_view()),
    path('<int:id>/delete/', DeleteProductView.as_view()),
    path('<int:product_id>/images/', AddProductImageView.as_view()),
    path('images/<int:image_id>/', DeleteProductImageView.as_view()),
]
