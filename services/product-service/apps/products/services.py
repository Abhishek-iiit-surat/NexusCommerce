
from .models import Category, Product, ProductImage
from .exceptions import ProductNotFoundError, CategoryNotFoundError, PermissionDeniedError, ProductImageNotFoundException
from django.core.paginator import Paginator
from django.utils.text import slugify

class CategoryService:

    def get_all_categories(self):
        return Category.objects.filter(is_active=True)
    
    def get_category(self,id):
        
        category = Category.objects.filter(id=id, is_active=True).first()
        if not category:
            raise CategoryNotFoundError(f"Category with id {id} not found.")
        return category
    
    def create_category(self,**data):
        data['slug'] = slugify(data['name'])
        category = Category.objects.create(**data) 
        return category
    
    def update_category(self,id, **data):
        category = Category.objects.filter(id = id, is_active = True).first()
        if not category:
            raise CategoryNotFoundError(f"Category with id {id} not found.")
        if 'name' in data:
            data['slug'] = slugify(data['name'])
        for key, value in data.items():
            setattr(category, key, value)

        category.save()
        return category
    

class ProductService:

    def get_all_products(self,page=1, page_size=10, category_id=None):
        products = Product.objects.filter(is_active=True, category_id=category_id) if category_id else Product.objects.filter(is_active=True)
        paginator = Paginator(products, page_size)
        page_obj = paginator.get_page(page)
        return page_obj.object_list, paginator.num_pages
    
    def create_product(self,created_by_id,**data):
        data['slug'] = slugify(data['name'])
        product = Product.objects.create(created_by = created_by_id, **data)
        return product

    def get_product(self,id):
        product = Product.objects.filter(id=id, is_active=True).first()
        if not product:
            raise ProductNotFoundError(f"Product with id {id} not found.")
        return product
    
    def update_product(self,id,user_id ,**data):
        product = Product.objects.filter(id=id, is_active=True).first()
        if not product:
            raise ProductNotFoundError(f"Product with id {id} not found.")
        if product.created_by != user_id:
            raise PermissionDeniedError(f"you dont have permission to delete or update this product")
        for key, value in data.items():
            setattr(product, key, value)

        product.save()
        return product

    def delete_product(self,id, user_id):
        product = Product.objects.filter(id=id, is_active=True).first()
        if not product:
            raise ProductNotFoundError(f"Product with id {id} not found.")
        if product.created_by != user_id:
            raise PermissionDeniedError(f"you dont have permission to delete or update this product")
        product.is_active = False
        product.save()
        return product
    



class ProductImageService:

    def add_product_image(self,product_id, **data):
        is_default = data.get('is_primary', False)
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            raise ProductNotFoundError(f"Product with id {product_id} not found.")
        if is_default:
            ProductImage.objects.filter(product_id=product_id, is_primary=True).update(is_primary=False)
        image = ProductImage.objects.create(product=product, **data)
        return image
    
    def delete_image(self,image_id):
        image = ProductImage.objects.filter(id=image_id).first()
        if not image:
            raise ProductImageNotFoundException(f"Product image with id {image_id} not found.")
        
        product_id = image.product_id
        image.delete()  
        remaining_images = ProductImage.objects.filter(product_id = product_id).order_by('order')
        for index, img in enumerate(remaining_images, start=1):
            if img.order != index:
                img.order = index
                img.save()  
        return True

