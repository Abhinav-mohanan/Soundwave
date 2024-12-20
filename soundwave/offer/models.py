from django.db import models
from products.models import Brand,Product

# Create your models here.
 
class Product_offer(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    offer_percentage = models.DecimalField(max_digits=10,decimal_places=2)
    offer_name= models.CharField(max_length=50,null=True,blank=True)
    offer_details=models.TextField(null=True,blank=True)
    started_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add= True)
    
    class Meta:
        ordering = ['-created_at']

    

class Brand_offer(models.Model):
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    offer_percentage=models.DecimalField(max_digits=10,decimal_places=2)
    offer_name=models.CharField(null=True,blank=True)
    offer_details=models.TextField(null=True,blank=True)
    started_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    