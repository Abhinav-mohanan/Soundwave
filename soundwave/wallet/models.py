from django.db import models
from user.models import CustomUser


# Create your models here.

class Wallet(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    balance =models.DecimalField(max_digits=30,decimal_places=2,default=0.00)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Transaction(models.Model):

    TRANSACTION_CHOICES=[
        ('Credit','Credit'),
        ('Debit','Debit')
    ]
    wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE)
    details=models.CharField(max_length=100,blank=True,null=True)
    amount=models.DecimalField(max_digits=30,decimal_places=2,default=0.00)
    transaction_type=models.CharField(max_length=50,choices=TRANSACTION_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)