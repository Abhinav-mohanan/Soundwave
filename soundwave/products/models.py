from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to='category_images',null=True,blank=True)
    is_listed=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class  Subcategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategories')
    description=models.TextField(default=True,null=True)
    image =models.ImageField(upload_to='subcategory_images',null=True,blank=True)
    is_listed=models.BooleanField(null=True,default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

class Brand(models.Model):
    name=models.CharField(max_length=100,unique=True)
    is_listed=models.BooleanField(default=True,null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name='category_product')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True,related_name='brand_product')
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE,null=True,blank=True,related_name='subcategory_product')
    feature=models.CharField(max_length=100,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_listed=models.BooleanField(default=True,null=True)
    
    def __str__(self):
        return self.name
    

class Variant(models.Model):
    COLOR_CHOICES =[
        ('Black','Black'),
        ('White','White'),
        ('Red','Red'),
        ('Blue','Blue')
    ]

    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    color=models.CharField(max_length=50,choices=COLOR_CHOICES)
    stock=models.PositiveIntegerField()
    image1=models.ImageField(upload_to='product_images')
    image2=models.ImageField(upload_to='product_images',blank=True,null=True)
    image3=models.ImageField(upload_to='product_images',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_listed=models.BooleanField(default=True,null=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"



    