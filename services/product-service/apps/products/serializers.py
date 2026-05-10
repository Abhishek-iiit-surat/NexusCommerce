from rest_framework.serializers import ModelSerializer
from .models import Product, Category, ProductImage

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at','product']

class ProductSerializer(ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at','created_by','is_active']
        

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at', 'slug']


