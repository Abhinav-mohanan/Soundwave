from django.db import models
from user.models import CustomUser
from products.models import Variant

# Create your models here.

class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='carts')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'cart of {self.user.username}'
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        return self.items.count()
    
class Cartitem(models.Model):
    cartitem_id=models.AutoField(primary_key=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.variant.product.name} - {self.variant.color} X {self.quantity} '
    
    @property
    def total_price(self):
        return self.quantity * self.variant.product.price
    

class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    add_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user{self.user.username}'s wishlist items:{self.variant.product.name}"
