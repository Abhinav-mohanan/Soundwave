from django.db import models
from user.models import CustomUser
from products.models import Variant
from cart.models import Cart
from accounts.models import Address
import uuid
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD','cash on delivery'),
        ('RazorPay','Razor Pay'),
        ('wallet','wallet'),
    ]

    PAYMENT_STATUS_CHOICES =[
        ('Success','Success'),
        ('Pending','Pending'),
        ('Failure','Failure'),
    ]
    
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    tracking_number=models.CharField(max_length=20,unique=True,editable=False)
    shipping_address=models.ForeignKey(Address,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    payment_type=models.CharField(choices=PAYMENT_CHOICES)
    payment_status=models.CharField(choices=PAYMENT_STATUS_CHOICES)
    estimated_delivery_date=models.DateTimeField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    def save(self,*args,**kwargs):
        if not self.tracking_number:
            self.tracking_number=str(uuid.uuid4().hex[:8])
        if not self.estimated_delivery_date:
            self.estimated_delivery_date=timezone.now().date() + timedelta(days=2)
        super().save(*args,**kwargs)


class Order_items(models.Model):
    STATUS_CHOICES= [
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),

    ] 


    Orderitem_id = models.AutoField(primary_key=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Order Pending')
    subtotal_price= models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self):
        return f'{self.variant.product.name} (x{self.quantity})'
    


    