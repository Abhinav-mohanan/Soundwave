from django.db import models
from user.models import CustomUser
from django.utils import timezone

class Coupon(models.Model):
    # Choices for coupon type
    FIXED = 'fixed'
    PERCENTAGE = 'percentage'
    COUPON_TYPE_CHOICES = [
        (FIXED, 'Fixed Amount'),
        (PERCENTAGE, 'Percentage'),
    ]

    coupon_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, default=None)
    coupon_type = models.CharField(max_length=10,choices=COUPON_TYPE_CHOICES,)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)


class Couponusage(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE)
    user_at=models.DateTimeField(auto_now_add=True)

