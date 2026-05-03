
from .models import Category, Product, ProductImage
from .exceptions import ProductNotFoundException, CategoryNotFoundException, ProductImageNotFoundException
from django.core.paginator import Paginator

class CategoryService:

    def get_all_categories(self):
        return Category.objects.filter(is_active=True)
    
    def get_category(id):
        category = Category.objects.filter(id=id, is_active=True).first()
        if not category:
            raise CategoryNotFoundException(f"Category with id {id} not found.")
        return category
    
    def create_category(**data):
        category, status = Category.objects.create(**data) 
        return category, status
    
    def update_category(id, **data):
        category = Category.objects.filter(id = id, is_active = True).first()
        if not category:
            raise CategoryNotFoundException(f"Category with id {id} not found.")
        for key, value in data.items():
            setattr(category, key, value)

        category.save()
        return category
    

class ProductService:

    def get_all_products(page=1, page_size=10, category_id=None):
        products = Product.objects.filter(is_active=True, category_id=category_id) if category_id else Product.objects.filter(is_active=True)
        paginator = Paginator(products, page_size)
        page_obj = paginator.get_page(page)
        return page_obj.object_list, paginator.num_pages
    
    def get_product(id):
        product = Product.objects.filter(id=id, is_active=True).first()
        if not product:
            raise ProductNotFoundException(f"Product with id {id} not found.")
        return product
    
    def update_product(id, **data):
        product = Product.objects.filter(id=id, is_active=True).first()
        if not product:
            raise ProductNotFoundException(f"Product with id {id} not found.")
        for key, value in data.items():
            setattr(product, key, value)

        product.save()
        return product
    
    def delete_product(id):
        product = Product.objects.filter(id=id, is_active=True).first()
        if not product:
            raise ProductNotFoundException(f"Product with id {id} not found.")
        product.is_active = False
        product.save()
        return product
    



class ProductImageService:

    def add_product_image(product_id, **data):
        is_default = data.get('is_primary', False)
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if is_default:
            ProductImage.objects.filter(product_id=product_id, is_primary=True).update(is_primary=False)
        if not product:
            raise ProductNotFoundException(f"Product with id {product_id} not found.")
        image, status = ProductImage.objects.create(product=product, **data)
        return image, status
    
    def delete_image(image_id):
        image = ProductImage.objects.filter(id=image_id).first()
        if not image:
            raise ProductImageNotFoundException(f"Product image with id {image_id} not found.")
        image.delete()  # deleted from db must be deleted from cloudinary as well right, once deleted order must be reordered
        # Reorder the remaining images if necessary
        return True

