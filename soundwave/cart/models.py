from django.db import models
from user.models import CustomUser
from products.models import Variant
from django.utils.timezone import now
from offer.models import Product_offer, Brand_offer

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
    
    class Meta:
        ordering  = ['-created_at']
    
class Cartitem(models.Model):
    cartitem_id=models.AutoField(primary_key=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.variant.product.name} - {self.variant.color} X {self.quantity} '
    
    @property
    def effective_price(self):
        current_date = now().date()
        product = self.variant.product

        product_offer = Product_offer.objects.filter(
            product=product,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        brand_offer = Brand_offer.objects.filter(
            brand=product.brand,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        product_discount_price = None
        brand_discount_price = None

        if product_offer:
            product_discount_price = (
                product.price * (1 - (product_offer.offer_percentage / 100))
            )

        if brand_offer:
            brand_discount_price = (
                product.price * (1 - (brand_offer.offer_percentage / 100))
            )

        if product_discount_price is not None and brand_discount_price is not None:
            final_discount_price = min(product_discount_price, brand_discount_price)

        elif product_discount_price is not None:
            final_discount_price = product_discount_price

        elif brand_discount_price is not None:
            final_discount_price = brand_discount_price

        else:
            final_discount_price = product.price

        return round(final_discount_price, 0)
    
    @property
    def line_total(self):
        return self.effective_price * self.quantity
    
    class Meta:
        ordering  = ['-created_at']

    

class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    add_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user{self.user.username}'s wishlist items:{self.variant.product.name}"
